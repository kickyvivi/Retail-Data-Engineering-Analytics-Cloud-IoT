from google.cloud import bigquery

client = bigquery.Client.from_service_account_json("C:/bigquery_service_account.json")

query = "SELECT table_name FROM `retail-iot-project.staging.INFORMATION_SCHEMA.TABLES`"
query_job = client.query(query)

for row in query_job:
    print(row["table_name"])
