import jaydebeapi

# Path to the Simba JDBC driver JAR file
jdbc_driver_path = "C:/apache-hop-client-2.11.0/hop/lib/jdbc/GoogleBigQueryJDBC42.jar"

# Database connection URL
jdbc_url = (
    "jdbc:bigquery://https://www.googleapis.com/bigquery/v2:443;"
    "ProjectId=retail-iot-project;"
    "OAuthType=0;"
    "OAuthServiceAcctEmail=data-generator@retail-iot-project.iam.gserviceaccount.com;"
    "OAuthPvtKeyPath=C:/bigquery_service_account.json;"
    "DatasetId=staging;"
)

# JDBC driver class for Simba BigQuery
jdbc_driver_class = "com.simba.googlebigquery.jdbc42.Driver"

# Empty credentials (BigQuery uses service account key instead)
jdbc_username = ""
jdbc_password = ""

try:
    # Establish the connection
    conn = jaydebeapi.connect(
        jdbc_driver_class,
        jdbc_url,
        [jdbc_username, jdbc_password],
        jdbc_driver_path,
    )
    print("Connection successful!")

    # Create a cursor to execute queries
    cursor = conn.cursor()

    # Test query to list tables in the dataset
    test_query = "SELECT table_name FROM information_schema.tables"
    cursor.execute(test_query)
    tables = cursor.fetchall()

    print("Tables in the dataset:")
    for table in tables:
        print(table)

    # Close the connection
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error occurred: {e}")
