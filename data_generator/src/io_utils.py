import csv
import shutil
import os
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

def save_to_csv(data, output_dir, file_name):
    """
    Save data to a CSV file.

    Args:
        data (list of dict): Data to save.
        output_dir (str): Directory to save the file.
        file_name (str): Name of the file.

    Returns:
        str: Full path to the saved file.
    """
    file_path = os.path.join(output_dir, file_name)
    
    # Write the CSV file normally
    temp_file_path = file_path + ".tmp"
    with open(temp_file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    # Read the file and add a space after commas
    with open(temp_file_path, mode="r") as file, open(file_path, mode="w", newline="") as final_file:
        for line in file:
            final_file.write(line.replace(",", ", "))

    # Remove the temporary file
    os.remove(temp_file_path)
    
    return file_path

def archive_file(file_path, archive_dir):
    """
    Move a file to the archive directory.

    Args:
        file_path (str): Path to the file.
        archive_dir (str): Archive directory.
    """
    os.makedirs(archive_dir, exist_ok=True)
    shutil.move(file_path, archive_dir)
    print(f"File archived to {archive_dir}")

