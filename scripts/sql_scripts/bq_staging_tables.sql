-- ### Staging Tables ###

-- stg_product
CREATE TABLE staging.stg_product (
    product_id INT64,
    product_name STRING,
    category STRING,
    subcategory STRING,
    brand STRING,
    price FLOAT64,
    update_type STRING, -- I/U/D for Change Data Capture
    insert_timestamp TIMESTAMP,
    processed_flag BOOLEAN DEFAULT FALSE
)
OPTIONS (
    description = "Staging table for product data"
);

-- stg_promotion
CREATE TABLE staging.stg_promotion (
    promotion_id INT64,
    promotion_name STRING,
    promotion_type STRING, -- $OFF, %OFF, BOGO
    discount_value FLOAT64,
    buy_quantity INT64,
    get_quantity INT64,
    start_date DATE,
    end_date DATE,
    status STRING, -- DRAFT, FINAL, CANCEL
	created_at TIMESTAMP,
	insert_timestamp TIMESTAMP,
    processed_flag BOOLEAN DEFAULT FALSE
)
OPTIONS (
    description = "Staging table for promotion data"
);

-- stg_promotion_items
CREATE TABLE staging.stg_promotion_items (
	promotion_id INT64,
	promotion_type STRING,
	item_type STRING, 
	product_id INT64,
	status STRING,
	created_at TIMESTAMP,
	updated_at TIMESTAMP,
	processed_flag BOOLEAN DEFAULT FALSE
)
OPTIONS (
	description = "Staging table for promotion line item data"
);

-- stg_customer
CREATE TABLE staging.stg_customer (
	customer_id INT64,
	first_name STRING,
	last_name STRING,
	email STRING,
	age INT64,
	city STRING,
	state STRING,
	country STRING,
	postal_code INT64,
	insert_timestamp TIMESTAMP,
	processed_flag BOOLEAN DEFAULT FALSE
)
OPTIONS (
	description = "Staging table for customer data"
);

-- stg_iot_cart_activity
CREATE TABLE staging.stg_iot_cart_activity (
	visit_id INT64,
	cart_id STRING,
	store_id INT64,
	customer_id INT64,
	json_message STRING,
	message_timestamp TIMESTAMP,
	insert_timestamp TIMESTAMP,
	processed_flag BOOLEAN DEFAULT FALSE
)
OPTIONS (
	description = "Staging table for raw IoT cart data"
);

-- stg_fact_sales
CREATE TABLE staging.stg_fact_sales(
	promotion_id INT64,
	product_id INT64,
	store_id INT64,
	customer_id INT64,
	record_timestamp TIMESTAMP,
	register_id INT64,
	transaction_id STRING,
	record_type STRING,
	sales_quantity FLOAT64,
	sales_amount FLOAT64,
	discounted_amount FLOAT64,
	insert_timestamp TIMESTAMP, 
	processed_flag BOOLEAN DEFAULT FALSE
)
OPTIONS (
	description = "Staging table for sales data"
);
