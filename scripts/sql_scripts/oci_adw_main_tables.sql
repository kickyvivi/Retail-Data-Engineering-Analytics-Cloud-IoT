CREATE TABLE retail_iot_project.dim_store (
    store_sk NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
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
    is_active CHAR(1) DEFAULT 'Y',
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);


CREATE TABLE retail_iot_project.dim_inventory (
    inventory_sk NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    product_sk NUMBER,
    store_sk NUMBER,
    stock_level NUMBER,
	reorder_level NUMBER,
    is_active CHAR(1) DEFAULT 'Y',
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);