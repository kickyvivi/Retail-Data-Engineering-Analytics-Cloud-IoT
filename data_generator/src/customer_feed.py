import os
from faker import Faker
import logging
from datetime import datetime
from io_utils import BigQueryClient, save_to_csv, archive_file
# from dependencies import fetch_customer_data
from config_loader import load_config

# Initialize Faker
fake = Faker()

# Config paths
BIGQUERY_CONFIG_PATH = "config/config.json"

# Load configurations
bigquery_config = load_config(BIGQUERY_CONFIG_PATH)
project_id = bigquery_config["bigquery"]["project_id"]
dataset_id = bigquery_config["bigquery"]["dataset_id"]

# Directories
OUTPUT_DIR = "output/customer/"
ARCHIVE_DIR = os.path.join(OUTPUT_DIR, "archive/")

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Set up logging
LOG_DIR = "logs/"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "customer_feed.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

def generate_customer_feed():
    """
    Generate the customer feed CSV file.
    """
    try:
        logger.info("Starting customer feed generation.")
        
        # Initialize BigQuery client
        bigquery_client = BigQueryClient()
        logger.info("BigQuery client initialized.")

        # Fetch the max customer ID from BigQuery
        query = f"SELECT MAX(customer_id) AS max_customer_id FROM `{project_id}.{dataset_id}.dim_customer`"
        result = bigquery_client.fetch_data(query)
        logger.info("Fetched max customer ID from BigQuery.")

        # Ensure max_customer_id is an integer (default to 1000 if None or not found)
        max_customer_id = result[0].get("max_customer_id", 1000) if result else 1000
        max_customer_id = max_customer_id if max_customer_id is not None else 1000
        logger.info(f"Max customer ID retrieved: {max_customer_id}")

        # Generate new customer data starting from max_customer_id + 1
        start_id = max_customer_id + 1
        new_customer_data = [
            {
                "customer_id": start_id + i,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "age": fake.random_int(min=18, max=75),
                "city": fake.city(),
                "state": fake.state_abbr(),
                "country": "US",
                "postal_code": fake.zipcode(),
            }
            for i in range(100)
        ]
        logger.info(f"Generated {len(new_customer_data)} new customer records.")

        # Save data to CSV
        current_date = datetime.now().strftime("%Y%m%d")
        file_name = f"raw_customer_{current_date}.csv"
        file_path = save_to_csv(new_customer_data, OUTPUT_DIR, file_name)
        logger.info(f"Customer feed saved to {file_path}.")

        # Archive the file (simulate post-ingestion retention)
        archive_file(file_path, ARCHIVE_DIR)
        logger.info(f"Customer feed archived to {ARCHIVE_DIR}.")

        print(f"Customer feed generated and saved to {file_path}")
        logger.info("Customer feed generation completed successfully.")

    except Exception as e:
        logger.error(f"Error during customer feed generation: {e}")
        raise

if __name__ == "__main__":
    generate_customer_feed()
