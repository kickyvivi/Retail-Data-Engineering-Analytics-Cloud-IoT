import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from datetime import datetime

# Define the pipeline options
class BeamOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--input', required=True, help='GCS input file path')
        parser.add_argument('--output_table', required=True, help='BigQuery output table')

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
        'insert_timestamp': datetime.utcnow().isoformat(),
        'processed_flag': 'FALSE'
    }

# Main pipeline
def run(argv=None):
    options = BeamOptions(argv)
    with beam.Pipeline(options=options) as p:
        (
            p
            | "Read CSV from GCS" >> beam.io.ReadFromText(options.input, skip_header_lines=1)
            | "Transform Data" >> beam.Map(transform_data)
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                options.output_table,
                schema=(
                    'customer_id:INTEGER,first_name:STRING,last_name:STRING,email:STRING,'
                    'age:INTEGER,city:STRING,state:STRING,country:STRING,postal_code:INTEGER,'
                    'insert_timestamp:TIMESTAMP,processed_flag:BOOLEAN'
                ),
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )

if __name__ == "__main__":
    run()
