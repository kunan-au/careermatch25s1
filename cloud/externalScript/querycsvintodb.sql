-- Create and use the database
CREATE DATABASE IF NOT EXISTS imba;
USE imba;

-- Create tables
CREATE TABLE aisles (
    aisle_id BIGINT PRIMARY KEY,
    aisle VARCHAR(255)
);

CREATE TABLE departments (
    department_id BIGINT PRIMARY KEY,
    department VARCHAR(255)
);

CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    product_name VARCHAR(255),
    aisle_id BIGINT,
    department_id BIGINT,
    FOREIGN KEY (aisle_id) REFERENCES aisles(aisle_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    user_id BIGINT,
    eval_set VARCHAR(50),
    order_number BIGINT,
    order_dow BIGINT,
    order_hour_of_day BIGINT,
    days_since_prior_order DOUBLE
);

-- Two tables for order products (prior and train)
CREATE TABLE order_products_prior (
    order_id BIGINT,
    product_id BIGINT,
    add_to_cart_order BIGINT,
    reordered BIGINT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE order_products_train (
    order_id BIGINT,
    product_id BIGINT,
    add_to_cart_order BIGINT,
    reordered BIGINT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Load data from CSV files
-- Note: Make sure local_infile is enabled. Double backslashes are used for Windows paths.
-- aisles
LOAD DATA LOCAL INFILE 'C:\\Users\\KA\\Downloads\\aisles.csv'
INTO TABLE aisles
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(aisle_id, aisle);

-- departments
LOAD DATA LOCAL INFILE 'C:\\Users\\KA\\Downloads\\departments.csv'
INTO TABLE departments
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(department_id, department);

-- products
LOAD DATA LOCAL INFILE 'C:\\Users\\KA\\Downloads\\products.csv'
INTO TABLE products
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(product_id, product_name, aisle_id, department_id);

-- orders
LOAD DATA LOCAL INFILE 'C:\\Users\\KA\\Downloads\\orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(order_id, user_id, eval_set, order_number, order_dow, order_hour_of_day, days_since_prior_order);

-- order_products_prior
LOAD DATA LOCAL INFILE 'C:\\Users\\KA\\Downloads\\order_products__prior.csv'
INTO TABLE order_products_prior
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(order_id, product_id, add_to_cart_order, reordered);

-- order_products_train
LOAD DATA LOCAL INFILE 'C:\\Users\\KA\\Downloads\\order_products__train.csv'
INTO TABLE order_products_train
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(order_id, product_id, add_to_cart_order, reordered);