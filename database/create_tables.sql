-- This script is for create tables of project 'customer_transaction'

-- #Create Database
-- The database was previously created in order to be able to work on it.
-- create database customer_transaction;

-- #Create Tables

-- Products
drop table if exists products;
create table products(
	product_id serial primary key, 
    brand VARCHAR(100) default 'unmarked',
    product_line VARCHAR(100),
    product_class VARCHAR(100),
    product_size VARCHAR(100)
);
-- Current Customer
drop table if exists current_customers;
create table current_customers(
    customer_id serial primary key,
    name VARCHAR(150) default 'NN',
    gender VARCHAR(150),
    past_3_years_bike_related_purchases INT,
    birth_date DATE check(birth_date > '1840-01-01'),
    age numeric check(age > 10),
    job_title VARCHAR(150),
    job_industry_category VARCHAR(150),
    wealth_segment VARCHAR(150),
    deceased_indicator VARCHAR(150),
    owns_car BOOL,
    tenure numeric,
    address VARCHAR(150),
    postcode INT,
    state VARCHAR(150),
    country VARCHAR(150),
    property_valuation INT
);
-- Transaction
drop table if exists transactions;
create table transactions(
	transaction_id serial,
    customer_id INT not null,
    transaction_date DATE check(transaction_date > '1900-01-01'),
    online_order bool,
    order_status VARCHAR(100),
    list_price numeric check(list_price > 0),
    standard_cost numeric check(standard_cost > 0),
    product_first_sold_date numeric,
    product_id INT not null,
    primary key (transaction_id),
    constraint fk_customer
    	foreign key (customer_id)
    		references current_customers(customer_id)
    		on delete set null,
    constraint fk_product
    	foreign key (product_id)
    		references products(product_id)
    		on delete set null
);
-- Targeted Customer
drop table if exists target_customers;
create table target_customers(
	target_id serial primary key,
   	first_name VARCHAR(150) default 'NN',
    last_name VARCHAR(150) default 'NN',
    gender VARCHAR(150),
    past_3_years_bike_related_purchases INT,
    birth_date DATE check(birth_date > '1900-01-01'),
    job_title VARCHAR(150),
    job_industry_category VARCHAR(150),
    wealth_segment VARCHAR(150),
    deceased_indicator VARCHAR(150),
    owns_car BOOL,
    tenure INT,
    address VARCHAR(150),
    postcode INT,
    state VARCHAR(150),
    country VARCHAR(150),
    property_valuation INT
);





