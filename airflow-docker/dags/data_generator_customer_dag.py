from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.models import Variable
import os

# Initialize PROJECT_HOME
PROJECT_HOME = Variable.get('PROJECT_HOME')

# output_direcotory = os.path.join(PROJECT_HOME, "shared-volume/output/customer")
# file_path = os.path.join(output_direcotory, "raw_customer_{{ ds_nodash }}.csv")

# Convert Windows path to UNIX-compatible path for Docker
output_directory = os.path.abspath(os.path.join(PROJECT_HOME, "shared_volume/output/customer"))
output_directory = output_directory.replace("\\", "/")  # Ensures compatibility

file_path = os.path.join(output_directory, "raw_customer_{{ ds_nodash }}.csv")
file_path = file_path.replace("\\", "/")  # Convert to UNIX format

# Default arguments
default_args = {
    'owner': 'airflow',
    'email_on_failure': True,
    'email_on_retry': False,
    'email': Variable.get('alert_email'),
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),

}


# Define DAG
with DAG(
    dag_id='customer_data_generation_dag',
    default_args=default_args,
    description='Generate customer feed using data generator and upload feed to gcs',
    schedule_interval="0 19 * * *",
    start_date=datetime(2025, 2, 2),
    catchup=False,
    tags=['data_generation', 'customer_feed'],
) as dag:

    # Task 1: Run the data generator docker container
    generate_data = DockerOperator(
        task_id='run_customer_data_generator',
        image='data-generator-image:latest',
        api_version='auto',
        auto_remove=True,
        command='python -m data_generator.src.data_generator --feed customer --records 100',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        volumes=[f"{output_directory}:/app/data_generator/output/customer"]
    )

    # Task 2: Upload the generated data to GCS
    upload_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_to_gcs',
        src=file_path,
        dst='output/customer/raw_customer_{{ ds_nodash }}.csv',
        bucket='retail-iot-project-data',
        gcp_conn_id="google_cloud_default"
    )

    # Task 3: Cleanup local files after upload
    cleanup = BashOperator(
        task_id='cleanup_local_file',
        bash_command=f'rm -f {file_path}'
    )

    # Set task dependencies
    generate_data >> upload_to_gcs >> cleanup