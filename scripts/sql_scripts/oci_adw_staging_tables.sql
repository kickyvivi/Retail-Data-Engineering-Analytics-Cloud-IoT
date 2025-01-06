CREATE TABLE retail_iot_project.stg_store (
    store_id NUMBER,
    store_name VARCHAR2(10),
    street VARCHAR2(200),
    city VARCHAR2(100),
    state VARCHAR2(2),
    region VARCHAR2(50),
    country VARCHAR2(50),
    postal_code NUMBER,
    store_open_date DATE,
    store_close_date DATE,
    insert_timestamp TIMESTAMP,
    processed_flag CHAR(1) DEFAULT 'N'
);

CREATE TABLE retail_iot_project.stg_inventory (    
    product_id NUMBER,
    store_id NUMBER,
    stock_level NUMBER,
	reorder_level NUMBER
);