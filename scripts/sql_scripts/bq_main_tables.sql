-- ### Main Tables ###

-- dim_product
CREATE TABLE main.dim_product (
    product_sk INT64 NOT NULL,
    product_id INT64,
    product_name STRING,
    category STRING,
    subcategory STRING,
    brand STRING,
    price FLOAT64,
    is_active BOOLEAN DEFAULT TRUE,
    is_current BOOLEAN DEFAULT TRUE,
    scd_start_date DATE,
    scd_end_date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
OPTIONS (
    description = "Slowly Changing Dimension table for product data"
);

-- dim_promotion
CREATE TABLE main.dim_promotion (
    promotion_sk INT64 NOT NULL,
    promotion_id INT64,
    promotion_name STRING,
    promotion_type STRING,
    discount_value FLOAT64,
    buy_quantity INT64,
    get_quantity INT64,
    start_date DATE,
    end_date DATE,
    status STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
OPTIONS (
    description = "Dimension table for promotion data"
);

-- dim_promotion_items
CREATE TABLE main.dim_promotion_items (
	promotion_item_sk INT64 NOT NULL,
	promotion_id INT64,
	promotion_type STRING,
	item_type STRING,
	product_sk INT64,
	product_id INT64,
	status STRING,
	created_at TIMESTAMP,
	updated_at TIMESTAMP
)
OPTIONS (
	description = "Dimension table for promotion line item data"
);

-- dim_customer
CREATE TABLE main.dim_customer (
	customer_sk INT64 NOT NULL,
	customer_id INT64,
	first_name STRING,
	last_name STRING,
	email STRING,
  age INT64,
	city STRING,
	state STRING,
	country STRING,
	postal_code INT64,
	is_current BOOLEAN DEFAULT TRUE,
	scd_start_date DATE,
	scd_end_date DATE,
	created_at TIMESTAMP,
	updated_at TIMESTAMP
)
OPTIONS (
	description = "Slowly Changing Dimension table for customer data"
);

-- iot_cart_activity
CREATE TABLE main.iot_cart_activity (
	cart_activity_sk INT64 NOT NULL,
	visit_id INT64,
	cart_id STRING,
	store_id INT64,
	customer_id INT64,
	aisle_id INT64,
	aisle_name STRING,
	duration_in_aisle FLOAT64,
	duration_at_checkout FLOAT64,
	message_timestamp TIMESTAMP,
	created_at TIMESTAMP,
	updated_at TIMESTAMP
)
OPTIONS (
	description = "Dimension table for IoT cart activity data"
);

-- iot_cart_activity_customervisit_snapshot
CREATE TABLE main.iot_cart_activity_customervisit_snapshot(
    customervisit_sk INT64 NOT NULL,
    customer_visit_id STRING, -- store_id + visit_id + customer_id
    customer_id INT64,
    store_id INT64,
    cart_id STRING,
    aisle ARRAY<STRUCT<
        aisle_id INT64,
        aisle_name STRING,
        duration_in_aisle FLOAT64>>,
    duration_at_checkout FLOAT64,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
OPTIONS (
    description = "Snapshot table for customer visits using IoT cart activity"
);

-- fact_promotion_sales
CREATE TABLE main.fact_promotion_sales (
    promotion_sales_sk INT64 NOT NULL,
    transaction_id STRING,
    transaction_lineitems ARRAY<STRUCT<
		transaction_line_id STRING, -- transaction_id + product_id
        product_sk INT64,
        promotion_sk INT64,
        sales_quantity FLOAT64,
        sales_amount FLOAT64,
        discounted_amount FLOAT64>>,
    total_sales_quantity FLOAT64,
    total_sales_amount FLOAT64,
    total_discounted_amount FLOAT64,
    store_sk INT64,
    customer_sk INT64,
    date_key INT64,
    date DATE,
    audit_sk INT64,
    register_id INT64,
    sale BOOLEAN,
    sale_timestamp TIMESTAMP,
    settlement BOOLEAN,
    settlement_timestamp TIMESTAMP,
    delivery BOOLEAN,
    delivery_timestamp TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
PARTITION BY date
CLUSTER BY store_sk
OPTIONS (
    description = "Fact table for promotion sales data"
);

-- fact_store_sales_weekly
CREATE TABLE main.fact_store_sales_weekly (
	weekly_sales_sk INT64 NOT NULL,
	store_sk INT64,
	week_start_date DATE,
	week_end_date DATE,
	business_period INT64,
	total_sales_amount FLOAT64,
	total_units_sold FLOAT64,
	created_at TIMESTAMP,
	updated_at TIMESTAMP
)
PARTITION BY week_start_date
CLUSTER BY store_sk
OPTIONS (
	description = "Fact table for aggregated weekly store sales data"
);

-- dim_audit
CREATE TABLE main.dim_audit(
	audit_sk INT64 NOT NULL,
	overall_quality_rating INT64,
	complete_flag BOOLEAN,
	screen_failed_flag BOOLEAN,
	screen_failed STRING,
	screen_fail_description STRING,
	ETL_timestamp TIMESTAMP
)
OPTIONS (
	description = "Audit table for fact_promotion_sales table"
);

-- dim_date
CREATE TABLE main.dim_date AS
WITH calendar AS (
  SELECT
    DATE_ADD(DATE('2023-12-31'), INTERVAL n DAY) AS curr_date
  FROM
    UNNEST(GENERATE_ARRAY(1, 3000)) AS n
)
SELECT
  FORMAT_DATE('%m%d%Y', curr_date) AS datekey,
  curr_date AS date,
  FORMAT_TIMESTAMP('%A', TIMESTAMP(curr_date)) AS week_day_full,
  FORMAT_TIMESTAMP('%a', TIMESTAMP(curr_date)) AS week_day_short,
  EXTRACT(DAYOFWEEK FROM curr_date) AS day_num_of_week,
  EXTRACT(DAY FROM curr_date) AS day_num_of_month,
  EXTRACT(DAYOFYEAR FROM curr_date) AS day_num_of_year,
  CONCAT(FORMAT_TIMESTAMP('%b', TIMESTAMP(curr_date)), '-', EXTRACT(YEAR FROM curr_date)) AS month_id,
  
  -- Corrected month_time_span
  EXTRACT(DAY FROM LAST_DAY(curr_date)) AS month_time_span,
  
  -- Corrected month_end_date
  LAST_DAY(curr_date) AS month_end_date,
  
  CONCAT(FORMAT_TIMESTAMP('%b', TIMESTAMP(curr_date)), ' ', EXTRACT(YEAR FROM curr_date)) AS month_short_desc,
  CONCAT(FORMAT_TIMESTAMP('%B', TIMESTAMP(curr_date)), ' ', EXTRACT(YEAR FROM curr_date)) AS month_long_desc,
  FORMAT_TIMESTAMP('%b', TIMESTAMP(curr_date)) AS month_short,
  FORMAT_TIMESTAMP('%B', TIMESTAMP(curr_date)) AS month_long,
  EXTRACT(MONTH FROM curr_date) AS month_num_of_year,
  CONCAT('Q', EXTRACT(QUARTER FROM curr_date), '-', EXTRACT(YEAR FROM curr_date)) AS quarter_id,
  
  -- Corrected quarter_time_span
  COUNT(*) OVER (
    PARTITION BY EXTRACT(QUARTER FROM curr_date), EXTRACT(YEAR FROM curr_date)
  ) AS quarter_time_span,
  
  -- Corrected quarter_end_date
  MAX(curr_date) OVER (
    PARTITION BY EXTRACT(QUARTER FROM curr_date), EXTRACT(YEAR FROM curr_date)
  ) AS quarter_end_date,
  
  EXTRACT(QUARTER FROM curr_date) AS quarter_num_of_year,
  CAST(EXTRACT(YEAR FROM curr_date) AS STRING) AS year_id,
  
  -- Corrected year_time_span
  COUNT(*) OVER (PARTITION BY EXTRACT(YEAR FROM curr_date)) AS year_time_span,
  
  -- Corrected year_end_date
  MAX(curr_date) OVER (PARTITION BY EXTRACT(YEAR FROM curr_date)) AS year_end_date
FROM
  calendar
ORDER BY
  curr_date;

--