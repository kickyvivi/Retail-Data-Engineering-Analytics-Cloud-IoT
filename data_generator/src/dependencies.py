from google.cloud import bigquery

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
