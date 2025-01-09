import pandas as pd
from io_utils import get_oracle_connection, BigQueryClient

def fetch_customer_data(bigquery_client, project_id, dataset_id):
    """Fetches customer data from BigQuery."""
    query = f"""
        SELECT customer_id, first_name, last_name, age, email, city, state, country, postal_code
        FROM `{project_id}.{dataset_id}.dim_customer`
        WHERE is_current = TRUE
    """
    result = bigquery_client.fetch_data(query) # Fetch data as a list of dictionaries
    return pd.DataFrame(result)  # Convert to pandas DataFrame

def fetch_product_data(bigquery_client, project_id, dataset_id):
    """Fetches product data from BigQuery."""
    query = f"""
        SELECT product_id, product_name, category, subcategory, brand, price
        FROM `{project_id}.{dataset_id}.dim_product`
        WHERE is_current = TRUE
    """
    result = bigquery_client.fetch_data(query)
    return pd.DataFrame(result)  # Convert to pandas DataFrame

def fetch_promo_data(bigquery_client, project_id, dataset_id):
    """Fetches active promotions from BigQuery."""
    query = f"""
        SELECT promotion_id, promotion_type, discount_value, start_date, end_date
        FROM `{project_id}.{dataset_id}.dim_promotion`
        WHERE status = 'FINAL' AND start_date <= CURRENT_DATE() AND end_date >= CURRENT_DATE()
    """
    result = bigquery_client.fetch_data(query)
    return pd.DataFrame(result)  # Convert to pandas DataFrame

def fetch_store_data(oracle_connection):
    """Fetches store data from Oracle ADW."""
    query = """
        SELECT store_id, store_name, street, city, state, region, country, postal_code
        FROM retail_iot_project.dim_store
        WHERE is_active = 'Y'
    """
    return pd.read_sql(query, con=oracle_connection)

def fetch_inventory_data(oracle_connection):
    """Fetches inventory data from Oracle ADW."""
    query = """
        SELECT inventory_sk, product_sk, store_sk, stock_level, reorder_level
        FROM retail_iot_project.dim_inventory
        WHERE is_active = 'Y'
    """
    return pd.read_sql(query, con=oracle_connection)
