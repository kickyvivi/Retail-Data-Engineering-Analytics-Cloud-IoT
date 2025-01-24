import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import datetime as datetime
from common.src.config_loader import load_config
from common.src.logging_config import setup_logger

# Configuration path
GCS_CONFIG_PATH = "beam_pipelines/config/config.json"

# Load configuration
config = load_config(GCS_CONFIG_PATH)
pipeline_config = config["gcs"]["stg_customer"]

# Setup logger
logger = setup_logger('logs/pipelines/stg_customer.log')
logger.info(f"Loaded configuration: {pipeline_config}")

# Define the pipeline options
class BeamOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--input', default=pipeline_config["input_path"], help='GCS input file path')
        parser.add_argument('--output_table', default=pipeline_config["output_table"] , help='BigQuery output table')

# Function to transform the data
def transform_data(row):
    fields = row.split(',')
    return {
        'customer_id': int(fields[0]),
        'first_name': fields[1],
        'last_name': fields[2],
        'email': fields[3],
        'age': int(fields[4]),
        'city': fields[5],
        'state': fields[6],
        'country': fields[7],
        'postal_code': fields[8],
        'insert_timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'processed_flag': 'FALSE'
    }

# Main pipeline
def run(argv=None):
    # Instantiate BeamOptions to parse command-line arguments
    options = BeamOptions(argv)

    # Extract options
    runner = pipeline_config["runner"]
    temp_location = pipeline_config["temp_location"]
    input_path = options.get_all_options()['input']
    output_table = options.get_all_options()['output_table']

    # Set runner and temp location in Pipeline Options from Config json - Can be overridden from command line
    options.view_as(PipelineOptions).view_as(beam.options.pipeline_options.StandardOptions).runner = runner
    options.view_as(PipelineOptions).view_as(beam.options.pipeline_options.GoogleCloudOptions).temp_location = temp_location

    logger.info(f"Runner: {runner}, Temp Location: {temp_location}, Input Path: {input_path}, Output Table: {output_table}")

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Read CSV from GCS" >> beam.io.ReadFromText(input_path, skip_header_lines=1)
            | "Transform Data" >> beam.Map(transform_data)
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                output_table,
                schema=(
                    'customer_id:INTEGER,first_name:STRING,last_name:STRING,email:STRING,'
                    'age:INTEGER,city:STRING,state:STRING,country:STRING,postal_code:INTEGER,'
                    'insert_timestamp:TIMESTAMP,processed_flag:BOOLEAN'
                ),
                custom_gcs_temp_location=temp_location,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )

if __name__ == "__main__":
    run()
