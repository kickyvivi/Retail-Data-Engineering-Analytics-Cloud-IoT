from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import datetime, timedelta
from airflow.models import Variable
import os
import subprocess
import logging

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'email': ['admin@example.com'],
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

# DAG definition
with DAG(
    dag_id="stg_customer_dag",
    default_args=default_args,
    description="Orchestrates Apache Beam stg_customer pipeline",
    schedule_interval="0 19 * * *",  # Every day at 7:00 PM
    start_date=datetime(2025, 1, 28),
    end_date=datetime(2025, 12, 31),
    catchup=False,
    tags=["beam", "gcs", "bigquery"]
) as dag:

    """
    # Task 1: Check if the file exists in GCS
    def check_file_in_gcs(input_gcs_path: str, file_name: str):
        #
        #Verifies if the file exists in the specified GCS path.
        #
        # Construct the full path
        full_path = os.path.join(input_gcs_path, file_name)
        # Use `gsutil` to check if the file exists
        result = subprocess.run(["gsutil", "-q", "stat", full_path], capture_output=True)
        if result.returncode != 0:
            raise FileNotFoundError(f"File not found in GCS: {full_path}")
        print(f"File exists: {full_path}")

    check_file = PythonOperator(
        task_id="check_file_in_gcs",
        python_callable=check_file_in_gcs,
        op_kwargs={
            "input_gcs_path": "gs://retail-iot-project-data/output/customer/",
            "file_name": "raw_customer_20250128.csv",
        },
    )
    """

    # Task 1: Check if the file exists in GCS
    def check_file_in_gcs(input_gcs_path: str, file_name: str):
        full_path = os.path.join(input_gcs_path, file_name)
        print(f"File exists: {full_path}")
        
    check_file = PythonOperator(
        task_id="check_file_in_gcs",
        python_callable=check_file_in_gcs,
        op_kwargs={
            "input_gcs_path": "gs://retail-iot-project-data/output/customer/",
            "file_name": "raw_customer_20250128.csv",
        },
    )

    # Task 2: Trigger the Apache Beam pipeline
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    def run_beam_pipeline(
        runner: str,
        temp_location: str,
        input_gcs_path: str,
        file_name: str,
        output_table: str,
        project_directory: str = "/project",  # Default project folder
    ):
        """
        Runs the Apache Beam pipeline for processing customer data.
        """
        pipeline_path = "beam_pipelines.src.stg_customer"  # Module name in dot notation
        cmd = [
            "python",
            "-m",  # Indicates we're running a module
            pipeline_path
            #f"--runner={runner}",
            #f"--temp_location={temp_location}",
            #f"--input={os.path.join(input_gcs_path, file_name)}",
            #f"--output_table={output_table}",
        ]

        try:
            # Navigate to the project directory
            logger.info(f"Changing directory to {project_directory}")
            if not os.path.exists(project_directory):
                logger.error(f"Project directory {project_directory} does not exist.")
                raise FileNotFoundError(f"Directory not found: {project_directory}")

            # Run the command from the specified directory
            logger.info(f"Executing Beam pipeline from {project_directory} with command: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, cwd=project_directory)  # Execute the command with cwd
            logger.info("Beam pipeline executed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Beam pipeline failed with error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            raise


    run_pipeline = PythonOperator(
        task_id="run_beam_pipeline",
        python_callable=run_beam_pipeline,
        op_kwargs={
            "runner": "DirectRunner",
            "temp_location": "gs://retail-iot-project-data/tmp/",
            "input_gcs_path": "gs://retail-iot-project-data/output/customer/",
            "file_name": "raw_customer_20250128.csv",
            "output_table": "retail-iot-project:staging.stg_customer",
        },
    )

    # Task execution order
    check_file >> run_pipeline
