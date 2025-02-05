import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions, GoogleCloudOptions
from apache_beam.metrics import Metrics
import datetime as datetime
from common.src.config_loader import load_config
from common.src.logging_config import setup_logger
from common.src.list_files_gcs_bucket import get_file_from_bucket
from beam_pipelines.validation.screens import StgCustomerValidation
import os

"""
# Configuration path
GCS_CONFIG_PATH = "beam_pipelines/config/config.json"

# Load configuration
config = load_config(GCS_CONFIG_PATH)
pipeline_config = config["gcs"]["stg_customer"]
"""

# Setup logger
logger = setup_logger('logs/pipeline/stg_customer.log')
logger.info("********Execution Started********")
#logger.info(f"Loaded configuration: {pipeline_config}")

# Setup Metrics
#processed_rows = Metrics.counter('stg_customer', 'processed_rows')
#error_rows = Metrics.counter('stg_customer', 'error_rows')


# Define the pipeline options
class BeamOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            '--input', 
            required=True,
            help='GCS input file path'
        )
        parser.add_argument(
            '--output_table',
             required=True,
             help='BigQuery output table'
        )

# Custom DoFn for validation and transnsformation
class ValidateAndTransformFn(beam.DoFn):
    def __init__(self, validation_class):
        self.validation_class = validation_class
        # Setup metrics
        self.processed_counter = Metrics.counter("stg_customer", "processed_rows")
        self.error_counter = Metrics.counter("stg_customer", "error_rows")
        self.warning_counter = Metrics.counter("stg_customer", "warning_rows")

    def process(self, element):
        try:
            row_data = dict(zip(
                ["customer_id", "first_name", "last_name", "email", "age", "city", "state", "country", "postal_code"],
                element.split(",")
            ))
            validated_row, errors = self.validation_class.validate_and_correct_row(row_data)

            # Add insert_timestamp and processed_flag to validated data
            validated_row.update({'insert_timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'processed_flag': 'FAlSE'})

            if errors:
                if errors[0] == "Row missing column data":
                    # self.error_counter.inc()        
                    raise ValueError(errors[0])     # When the row is missing columns
                else:
                    self.warning_counter.inc()      # Warning when column screens fail, but row is processed with or without data correction
                    self.processed_counter.inc()    # Row is processed after error correction
                    logger.warning(f"Row Warnings: {errors} | Data: {element}")
                    yield validated_row             # yield row for further processing
            else:
                self.processed_counter.inc()
                yield validated_row
        except Exception as e:
            self.error_counter.inc()
            logger.error(f"Critical error during row validation: {e} | Row: {element}")

# Main pipeline
def run(argv=None):

    # Instantiate BeamOptions to parse command-line arguments
    options = BeamOptions(argv)

    # Parsing command line arguments passed from Orchestrator
    opts = options.get_all_options()
    runner = opts['runner']
    temp_location = opts['temp_location']
    input_path = opts['input']
    output_table = opts['output_table']

    # Configure the Beam pipeline options.
    options.view_as(StandardOptions).runner = runner
    options.view_as(GoogleCloudOptions).temp_location = temp_location

    # Initiliaze validation class
    validator = StgCustomerValidation()

    # Get file to process
    input_file = get_file_from_bucket(
        bucket_path=input_path,
        filename_template=r'raw_customer_\d{8}\.csv'
    )

    if not input_file:
        logger.error(f"No file found matching the template in gcs path: {input_path}")
        return
    
    logger.info(f"Processing file: {input_file}")

    # File validation
    try:
        logger.info(f"Validating file: {input_file}")
        file_validaton_result = validator.validate_file(
            file_path=input_file,
            expected_columns=[
                'customer_id', 'first_name', 'last_name', 'email', 'age','city', 'state', 'country', 'postal_code'
            ],
            filename_template=r'raw_customer_\d{8}\.csv'
        )
        if not file_validaton_result:
            logger.error(f"File validation returned False. Stopping pipeline execution.")
            return

    except ValueError as e:
        logger.error(f"Critical error during file validation: {e}")
        return

    logger.info("File validation passed. Starting pipeline execution.")
    
    # Pipeline execution
    try:
        logger.info(f"Pipeline started with Runner: {runner}, Temp Location: {temp_location}, Input Path: {input_path}, Output Table: {output_table}")
        
        with beam.Pipeline(options=options) as p:
            (
                p
                | "Read CSV from GCS" >> beam.io.ReadFromText(input_path, skip_header_lines=1)
                | "Validate and Transform Data" >> beam.ParDo(ValidateAndTransformFn(validator))
                | "Filter invalid rows" >> beam.Filter(lambda x: x is not None)
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
        # Wait for pipeline exeucution to complete before retrieving metrics
        logger.info("Write to BigQuery executed. Waiting for pipeline to complete.")
        #result = p.run()   # Not required as pipeline is executed inside the 'with' context
        result = p.result   # Retrieving metrics directly 
        result.wait_until_finish()

        # Retrieving metrics
        processed_metric = result.metrics().query(
            beam.metrics.MetricsFilter().with_name("processed_rows")
        )['counters']
        
        error_metric = result.metrics().query(
            beam.metrics.MetricsFilter().with_name("error_rows")
        )['counters']

        warning_metric = result.metrics().query(
            beam.metrics.MetricsFilter().with_name("warning_rows")
        )['counters']

        processed_count = processed_metric[0].committed if processed_metric else 0
        error_count = error_metric[0].committed if error_metric else 0
        warning_count = warning_metric[0].committed if warning_metric else 0
        total_count = processed_count + error_count
        
        logger.info("Pipeline execution completed successfully.")
        logger.info(f"Total rows: {total_count}")
        logger.info(f"Total processed rows: {processed_count}")
        logger.info(f"Total warning rows: {warning_count}")
        logger.info(f"Total error rows: {error_count}")
    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    run()
