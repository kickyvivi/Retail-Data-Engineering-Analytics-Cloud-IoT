from dependencies import BigQueryClient

if __name__ == "__main__":
    # Initialize the client
    bq_client = BigQueryClient()
    
    # Test the connection
    bq_client.test_connection()
    
    # Example query to fetch data
    query = "SELECT table_name FROM `retail-iot-project.main.INFORMATION_SCHEMA.TABLES` LIMIT 10"
    tables = bq_client.fetch_data(query)
    print("Fetched Tables:", tables)
