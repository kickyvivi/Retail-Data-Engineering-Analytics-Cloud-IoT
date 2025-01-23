import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

options = PipelineOptions()

with beam.Pipeline(options=options) as p:
    lines = p | beam.io.ReadFromText('gs://retail-iot-project-data/sample/sample.csv')
    rows = lines | beam.Map(lambda x: x.split(','))
    data = rows | beam.Map(lambda x: {'name': x[0], 'age': int(x[1]), 'city': x[2]})
    data | beam.io.WriteToBigQuery(
        'retail-iot-project:staging.beam_sample',
        schema='name:STRING,age:INTEGER,city:STRING',
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE
    )