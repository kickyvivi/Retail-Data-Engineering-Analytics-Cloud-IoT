import oracledb
import json
from google.cloud import bigquery

def get_oracle_connection(config_path):
    """
    Establish a connection to the Oracle ADB using TLS.

    Args:
        config_path (str): Path to the JSON configuration file.
    Returns:
        oracledb.Connection: Oracle database connection object.
    """
    # Load config
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Build the DSN
    dsn = f"(description=(retry_count=20)(retry_delay=3)" \
          f"(address=(protocol=tcps)(port={config['dsn']['port']})(host={config['dsn']['host']}))" \
          f"(connect_data=(service_name={config['dsn']['service_name']}))" \
          f"(security=(ssl_server_dn_match=yes)))"

    # Connect to the database
    connection = oracledb.connect(
        user=config["user"],
        password=config["password"],
        dsn=dsn
    )
    return connection

class BigQueryClient:
    def __init__(self):
        """Initialize the BigQuery Client."""
        self.client = bigquery.Client()

    def test_connection(self):
        """Test BigQuery connection by running a simple query."""
        try:
            query = "SELECT CURRENT_TIMESTAMP() as current_time"
            query_job = self.client.query(query)
            result = query_job.result()
            for row in result:
                print(f"Connection successful. Current BigQuery time: {row.current_time}")
        except Exception as e:
            print(f"Error connecting to BigQuery: {e}")
    
    def fetch_data(self, query):
        """
        Fetch data from BigQuery using a query.
        
        Args:
            query (str): SQL query to execute.
            
        Returns:
            List[Dict]: Query results as a list of dictionaries.
        """
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            return [dict(row) for row in results]
        except Exception as e:
            print(f"Error executing query: {e}")
            return []
