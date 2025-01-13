## SQL Scripts
- **staging_tables.sql**: Contains CREATE TABLE statements for staging tables.
- **main_tables.sql**: Contains CREATE TABLE statements for main dimension and fact tables.


## Structured representation of main tables:

### **dim_product**

| Column Name     | Data Type | Key Type      |
|-----------------|-----------|---------------|
| product_sk      | INT64     | Primary Key   |
| product_id      | INT64     |               |
| product_name    | STRING    |               |
| category        | STRING    |               |
| subcategory     | STRING    |               |
| brand           | STRING    |               |
| price           | FLOAT64   |               |
| is_active       | BOOLEAN   | Default: TRUE |
| is_current      | BOOLEAN   | Default: TRUE |
| scd_start_date  | DATE      |               |
| scd_end_date    | DATE      |               |
| created_at      | TIMESTAMP |               |
| updated_at      | TIMESTAMP |               |

### **dim_promotion**

| Column Name      | Data Type  | Key Type      |
|------------------|------------|---------------|
| promotion_sk     | INT64      | Primary Key   |
| promotion_id     | INT64      |               |
| promotion_name   | STRING     |               |
| promotion_type   | STRING     |               |
| discount_value   | FLOAT64    |               |
| buy_quantity     | INT64      |               |
| get_quantity     | INT64      |               |
| start_date       | DATE       |               |
| end_date         | DATE       |               |
| status           | STRING     |               |
| created_at       | TIMESTAMP  |               |
| updated_at       | TIMESTAMP  |               |

### **dim_promotion_items**

| Column Name      | Data Type  | Key Type      |
|------------------|------------|---------------|
| promotion_item_sk | INT64      | Primary Key   |
| promotion_id     | INT64      |               |
| promotion_type   | STRING     |               |
| item_type        | STRING     |               |
| product_sk       | INT64      |               |
| product_id       | INT64      |               |
| status           | STRING     |               |
| created_at       | TIMESTAMP  |               |
| updated_at       | TIMESTAMP  |               |

### **dim_customer**

| Column Name      | Data Type  | Key Type      |
|------------------|------------|---------------|
| customer_sk      | INT64      | Primary Key   |
| customer_id      | INT64      |               |
| first_name       | STRING     |               |
| last_name        | STRING     |               |
| email            | STRING     |               |
| age              | INT64      |               |
| city             | STRING     |               |
| state            | STRING     |               |
| country          | STRING     |               |
| postal_code      | INT64      |               |
| is_current       | BOOLEAN    |               |
| scd_start_date   | DATE       |               |
| scd_end_date     | DATE       |               |
| created_at       | TIMESTAMP  |               |
| updated_at       | TIMESTAMP  |               |

### **iot_cart_activity**

| Column Name         | Data Type  | Key Type      |
|---------------------|------------|---------------|
| cart_activity_sk    | INT64      | Primary Key   |
| visit_id            | INT64      |               |
| cart_id             | STRING     |               |
| store_id            | INT64      |               |
| customer_id         | INT64      |               |
| aisle_id            | INT64      |               |
| aisle_name          | STRING     |               |
| duration_in_aisle   | FLOAT64    |               |
| duration_at_checkout| FLOAT64    |               |
| message_timestamp   | TIMESTAMP  |               |
| created_at          | TIMESTAMP  |               |
| updated_at          | TIMESTAMP  |               |

### **iot_cart_activity_customervisit_snapshot**

| Column Name         | Data Type  | Key Type      |
|---------------------|------------|---------------|
| customervisit_sk    | INT64      | Primary Key   |
| customer_visit_id   | STRING     |               |
| customer_id         | INT64      |               |
| store_id            | INT64      |               |
| cart_id             | STRING     |               |
| aisle               | ARRAY<STRUCT<aisle_id INT64, aisle_name STRING, duration_in_aisle FLOAT64>> | |
| duration_at_checkout| FLOAT64    |               |
| created_at          | TIMESTAMP  |               |
| updated_at          | TIMESTAMP  |               |

### **fact_promotion_sales**

| Column Name               | Data Type  | Key Type      |
|---------------------------|------------|---------------|
| sales_sk                  | INT64      | Primary Key   |
| transaction_id            | STRING     |               |
| transaction_lineitems     | ARRAY<STRUCT<transaction_line_id STRING, product_sk INT64, promotion_sk INT64, sales_quantity FLOAT64, sales_amount FLOAT64, discounted_amount FLOAT64>> | |
| total_sales_quantity      | FLOAT64    |               |
| total_sales_amount        | FLOAT64    |               |
| total_discounted_amount   | FLOAT64    |               |
| store_sk                  | INT64      |               |
| register_id               | INT64      |               |
| customer_sk               | INT64      |               |
| date_key                  | INT64      |               |
| date                      | DATE       |               |
| audit_sk                  | INT64      |               |
| sale                      | BOOLEAN    |               |
| sale_timestamp            | TIMESTAMP  |               |
| settlement                | BOOLEAN    |               |
| settlement_timestamp      | TIMESTAMP  |               |
| delivery                  | BOOLEAN    |               |
| delivery_timestamp        | TIMESTAMP  |               |
| created_at                | TIMESTAMP  |               |
| updated_at                | TIMESTAMP  |               |

### **fact_store_sales_weekly**

| Column Name         | Data Type  | Key Type      |
|---------------------|------------|---------------|
| weekly_sales_sk     | INT64      | Primary Key   |
| store_sk            | INT64      |               |
| week_start_date     | DATE       | Partition Key |
| week_end_date       | DATE       |               |
| business_period     | INT64      |               |
| total_sales_amount  | FLOAT64    |               |
| total_units_sold    | FLOAT64    |               |
| created_at          | TIMESTAMP  |               |
| updated_at          | TIMESTAMP  |               |

### **dim_audit**

| Column Name            | Data Type  | Key Type      |
|------------------------|------------|---------------|
| audit_sk               | INT64      | Primary Key   |
| overall_quality_rating | INT64      |               |
| complete_flag          | BOOLEAN    |               |
| screen_failed_flag     | BOOLEAN    |               |
| screen_failed          | STRING     |               |
| screen_fail_description| STRING     |               |
| ETL_timestamp          | TIMESTAMP  |               |

### **dim_date**

| Column Name         | Data Type  | Key Type      |
|---------------------|------------|---------------|
| datekey             | STRING     | Primary Key   |
| date                | DATE       |               |
| week_day_full       | STRING     |               |
| week_day_short      | STRING     |               |
| day_num_of_week     | INT64      |               |
| day_num_of_month    | INT64      |               |
| day_num_of_year     | INT64      |               |
| month_id            | STRING     |               |
| month_time_span     | INT64      |               |
| month_end_date      | DATE       |               |
| month_short_desc    | STRING     |               |
| month_long_desc     | STRING     |               |
| month_short         | STRING     |               |
| month_long          | STRING     |               |
| month_num_of_year   | INT64      |               |
| quarter_id          | STRING     |               |
| quarter_time_span   | INT64      |               |
| quarter_end_date    | DATE       |               |
| quarter_num_of_year | INT64      |               |
| year_id             | STRING     |               |
| year_time_span      | INT64      |               |
| year_end_date       | DATE       |               |

### **dim_store**

| Column Name       | Data Type      | Key Type      |
|-------------------|----------------|---------------|
| store_sk          | NUMBER         | Primary Key   |
| store_id          | NUMBER         |               |
| store_name        | VARCHAR2(10)   |               |
| street            | VARCHAR2(200)  |               |
| city              | VARCHAR2(100)  |               |
| state             | VARCHAR2(2)    |               |
| region            | VARCHAR2(50)   |               |
| country           | VARCHAR2(50)   |               |
| postal_code       | NUMBER         |               |
| store_open_date   | DATE           |               |
| store_close_date  | DATE           |               |
| is_active         | CHAR(1)        |               |
| created_at        | TIMESTAMP      |               |
| updated_at        | TIMESTAMP      |               |

### **dim_inventory**

| Column Name       | Data Type      | Key Type      |
|-------------------|----------------|---------------|
| inventory_sk      | NUMBER         | Primary Key   |
| product_sk        | NUMBER         |               |
| store_sk          | NUMBER         |               |
| stock_level       | NUMBER         |               |
| reorder_level     | NUMBER         |               |
| is_active         | CHAR(1)        |               |
| created_at        | TIMESTAMP      |               |
| updated_at        | TIMESTAMP      |               | 
