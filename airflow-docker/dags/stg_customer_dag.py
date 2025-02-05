"""
Tasks:
  1. Validate the file in GCS. --> GCSObjectExistenceSensor
  2. Ensure the BigQuery table exists. --> BigQueryTableExistenceSensor
  3. Beam Pipeline --> BeamRunPythonPipelineOperator
        a. Trigger the Beam file validation pipeline.
        b. Trigger the Beam row validation and transformation pipeline.
        c. Load data into BigQuery.
  6. Send an email notification on pipeline failure. --> EmailOperator
  7. Archive the processed file in GCS. --> GCSToGCSOperator
"""  

from airflow import DAG
from airflow.datasets import Dataset
from airflow.providers.google.cloud.sensors.bigquery import BigQueryTableExistenceSensor
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.apache.beam.operators.beam import BeamRunPythonPipelineOperator
from airflow.operators.email import EmailOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.utils.dates import datetime, timedelta
from airflow.models import Variable
import os

# Initialize file paths
# PROJECT_HOME_AIRFLOW = Variable.get('PROJECT_HOME_AIRFLOW')
# BEAM_PIPELINE_PATH = os.path.join(PROJECT_HOME_AIRFLOW, 'beam_pipelines.src.stg_customer')
BEAM_PIPELINE_PATH = "beam_pipelines.src.stg_customer_orchestrated"


default_args = {
    'owner': 'airflow',
    'email_on_failure': True,
    'email_on_retry': False,
    'email': Variable.get('alert_email'),
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='beam_pipeline_dag',
    default_args=default_args,
    # Use the Dataset as the schedule trigger; this makes DAG2 a consumer.
    schedule=[Dataset("customer_feed_dataset")],
    description='Orchestrates Apache Beam pipeline for customer feed processing',
    start_date=datetime(2025, 2, 2),
    catchup=False,
    tags=['beam', 'gcs', 'bigquery']
) as dag:
    
    validate_file = GCSObjectExistenceSensor(
        task_id="validate_file_in_gcs",
        poke_interval=60,
        timeout=300,
        soft_fail="False",
        mode="reschedule",
        #exponential_backoff="False",
        #max_wait="None",
        silent_fail="False",
        never_fail="False",
        bucket=Variable.get("GCS_BUCKET"),
        object="output/customer/raw_customer_{{ ds_nodash }}.csv",
        #use_glob="False",
        google_cloud_conn_id="google_cloud_default",
        #impersonation_chain="None",
        #retry="DEFAULT_RETRY",
        deferrable=True
    ) 

    ensure_bq_table = BigQueryTableExistenceSensor(
        task_id="ensure_bq_table_exists",
        poke_interval=60,
        timeout=300,
        soft_fail="False",
        mode="reschedule",
        exponential_backoff="False",
        #max_wait="None",
        silent_fail="False",
        never_fail="False",
        #project_id=str(Variable.get("GOOGLE_CLOUD_PROJECT")),
        project_id=Variable.get("GOOGLE_CLOUD_PROJECT"),
        dataset_id="staging",
        table_id="stg_customer",
        gcp_conn_id="google_cloud_default",
        #impersonation_chain=None,
        deferrable=True
    )

    run_beam_pipeline = BeamRunPythonPipelineOperator(
        task_id="run_beam_pipeline",
        runner="DirectRunner",
        default_pipeline_options=None,
        pipeline_options={
                "input": "gs://retail-iot-project-data/output/customer/raw_customer_{{ ds_nodash }}.csv",
                "output_table": "retail-iot-project:staging.stg_customer",            
                "temp_location": "gs://retail-iot-project-data/tmp/"
            },
        #gcp_conn_id="google_cloud_default",
        #dataflow_config="None",
        py_file=BEAM_PIPELINE_PATH,
        py_interpreter="python3",
        py_options=["-m"],
        #py_requirements=["apache-beam[gcp]"],
        py_system_site_packages=False,
        deferrable=False,
    )

    archive_file = GCSToGCSOperator(
        task_id="archive_file",
        source_bucket=Variable.get("GCS_BUCKET"),
        source_object="output/customer/raw_customer_{{ ds_nodash }}.csv",
        #source_objects="None",
        #destination_bucket="None",
        destination_object="output/customer/archive/",
        #delimiter="None",
        move_object=True,
        replace="True",
        gcp_conn_id="google_cloud_default",
        #last_modified_time="None",
        #maximum_modified_time="None",
        #is_older_than="None",
        #impersonation_chain="None",
        source_object_required="False",
        exact_match="False",
        #match_glob="None",
    )

    send_failure_email = EmailOperator(
        task_id="send_failure_email",
        to=Variable.get("alert_email"),
        subject="Airflow: Beam pipeline failure notification",
        html_content="<h3>The Apache Beam pipeline for customer feed processing has failed. Please review the logs.</h3>",
        files="None",
        cc="None",
        bcc="None",
        mime_subtype="mixed",
        mime_charset="utf-8",
        conn_id="None",
        custom_headers="None",
        trigger_rule="one_failed"
    )

    validate_file >> ensure_bq_table >> run_beam_pipeline >> archive_file
    run_beam_pipeline >> send_failure_email
