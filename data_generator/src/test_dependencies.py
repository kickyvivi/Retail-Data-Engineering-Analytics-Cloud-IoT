from io_utils import get_oracle_connection, BigQueryClient
from dependencies import (
    fetch_customer_data,
    fetch_product_data,
    fetch_promo_data,
    fetch_store_data,
    fetch_inventory_data,
)

# Define the oracle config path
CONFIG_PATH = "config/oracle_config.json"

if __name__ == "__main__":
    # Initialize connections
    bigquery_client = BigQueryClient()
    oracle_connection = get_oracle_connection(CONFIG_PATH)
    
    # Fetch data
    customer_data = fetch_customer_data(bigquery_client, "retail-iot-project", "main")
    product_data = fetch_product_data(bigquery_client, "retail-iot-project", "main")
    promo_data = fetch_promo_data(bigquery_client, "retail-iot-project", "main")
    store_data = fetch_store_data(oracle_connection)
    inventory_data = fetch_inventory_data(oracle_connection)
    
    # Print results
    print("Customer Data:", customer_data.head())
    print("Product Data:", product_data.head())
    print("Promo Data:", promo_data.head())
    print("Store Data:", store_data.head())
    print("Inventory Data:", inventory_data.head())
