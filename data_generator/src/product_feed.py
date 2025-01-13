import os
import logging
from faker import Faker
from datetime import datetime
from io_utils import BigQueryClient, save_to_csv, archive_file
from config_loader import load_config
import random  # Import Python's random library

# Initialize Faker
fake = Faker()

# Config paths
BIGQUERY_CONFIG_PATH = "config/config.json"
CATEGORY_CONFIG_PATH = "config/categories.json"

# Load configurations
bigquery_config = load_config(BIGQUERY_CONFIG_PATH)
categories_config = load_config(CATEGORY_CONFIG_PATH)

project_id = bigquery_config["bigquery"]["project_id"]
dataset_id = bigquery_config["bigquery"]["dataset_id"]
categories = categories_config["Category"]

# Directories
OUTPUT_DIR = "output/product/"
ARCHIVE_DIR = os.path.join(OUTPUT_DIR, "archive/")

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# Set up logging
LOG_DIR = "logs/"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "product_feed.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

def generate_product_feed():
    """
    Generate the product feed CSV file.
    """
    try:
        logger.info("Starting product feed generation.")
        
        # Initialize BigQuery client
        bigquery_client = BigQueryClient()
        logger.info("BigQuery client initialized.")

        # Fetch the max product ID from BigQuery
        query = f"SELECT MAX(product_id) AS max_product_id FROM `{project_id}.{dataset_id}.dim_product`"
        result = bigquery_client.fetch_data(query)
        logger.info("Fetched max product ID from BigQuery.")

        # Ensure max_product_id is an integer (default to 10001 if None or not found)
        max_product_id = result[0].get("max_product_id", 10001) if result else 10001
        max_product_id = max_product_id if max_product_id is not None else 10001
        logger.info(f"Max product ID retrieved: {max_product_id}")

        # Generate new product data starting from max_product_id + 1
        start_id = max_product_id + 1
        new_product_data = [
            {
                "product_id": start_id + i,
                "product_name": f"{fake.word().capitalize()} {fake.word().capitalize()}",
                "category": category["Name"],
                "subcategory": random.choice(category["Subcategory"])["Name"],  # Fixed subcategory selection
                "brand": fake.company(),
                "price": round(fake.random_number(digits=3) / 10, 2),  # Price range: $0.10 - $99.99
            }
            for i, category in zip(range(100), random.choices(categories, k=100))  # Use random.choices directly
        ]
        logger.info(f"Generated {len(new_product_data)} new product records.")

        # Save data to CSV
        current_date = datetime.now().strftime("%Y%m%d")
        file_name = f"raw_product_{current_date}.csv"
        file_path = save_to_csv(new_product_data, OUTPUT_DIR, file_name)
        logger.info(f"Product feed saved to {file_path}.")

        # Archive the file (simulate post-ingestion retention)
        archive_file(file_path, ARCHIVE_DIR)
        logger.info(f"Product feed archived to {ARCHIVE_DIR}.")

        print(f"Product feed generated and saved to {file_path}")
        logger.info("Product feed generation completed successfully.")

    except Exception as e:
        logger.error(f"Error during product feed generation: {e}")
        raise

if __name__ == "__main__":
    generate_product_feed()
