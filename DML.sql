-- Group 56: Dania Magana and August Frisk

-- ####################################################################
-- The BROWSE customers.html Page
-- ####################################################################

-- get all Customers
SELECT customer_id AS ID, customer_name AS Name, customer_phone AS Phone, customer_email AS Email FROM Customers;

-- add a new Customer
INSERT INTO Customers (customer_name, customer_phone, customer_email) VALUES
(:nameInput, :phoneInput, :emailInput);

-- update a Customer
SELECT customer_id AS 'Customer ID', customer_name AS Name, customer_phone AS 'Phone Number', customer_email AS Email
FROM Customers
WHERE customer_id = :customer_id_selected_from_browse_customer_page;

UPDATE Customers
SET customer_name = :nameInput, customer_phone = :phoneInput, customer_email = :emailInput
WHERE customer_id = :customer_id_from_the_update_form;

-- delete a Customer
DELETE FROM Customers WHERE customer_id = :customer_id_selected_from_browse_customer_page;

-- ####################################################################
-- The BROWSE orders.html Page
-- ####################################################################

-- get all Orders
SELECT order_id AS ID, order_date AS Date, customer_id AS 'Customer ID', store_id AS 'Store ID', total_before_tax AS Price, SalesTaxes.sales_tax AS 'Sales Tax', order_total AS Total
FROM Orders
INNER JOIN SalesTaxes
ON Orders.sales_tax = SalesTaxes.sales_tax_id;

-- get all Customer IDs, Names, Phone Numbers, and Emails to populate Customer dropdown
SELECT customer_id, customer_name, customer_phone, customer_email FROM Customers;

-- get all Store IDs, Phones, Emails, and Addresses to populate Store dropdown
SELECT store_id, store_phone, store_email, CONCAT(Addresses.street_address, ', ', Cities.city, ', ', States.state, ' ', ZipCodes.zip_code) 
FROM Stores
INNER JOIN Addresses
ON Addresses.address_id = Stores.store_address
INNER JOIN Cities
ON Cities.city_id = Addresses.city
INNER JOIN States
ON States.state_id = Addresses.state
INNER JOIN ZipCodes
ON ZipCodes.zip_id = Addresses.zip_code;

-- get all Sales Taxes and States to populate Sales Tax dropdown
SELECT States.state, SalesTaxes.sales_tax
FROM SalesTaxes
INNER JOIN States
ON States.state_id = SalesTaxes.state;

-- get all Order Details
SELECT OrderDetails.order_detail_id AS ID, Orders.order_id AS 'Order ID', CONCAT(Products.product_description, ', ', ProductTypes.product_type, ', ', ProductConditions.product_condition) AS 'Product Description', order_quantity AS Quantity
FROM OrderDetails
INNER JOIN Orders
ON Orders.order_id = OrderDetails.order_id
INNER JOIN Products
ON Products.product_id = OrderDetails.product_id
INNER JOIN ProductTypes
ON ProductTypes.product_type_id = Products.product_type
INNER JOIN ProductConditions
ON ProductConditions.product_condition_id = Products.product_condition;

-- add a new Order
INSERT INTO Orders (order_date, customer_id, store_id, total_before_tax, sales_tax, order_total) VALUES
(:dateInput, :customer_id_from_dropdown_Input, :store_id_from_dropdown_Input, :total_before_tax_from_order_items_form, :sales_tax_from_dropdown_Input, :order_total_from_total_form);

-- ####################################################################
-- The BROWSE stores.html Page
-- ####################################################################

-- get all Stores
SELECT store_id AS ID, store_phone AS Phone, store_email AS Email, CONCAT(Addresses.street_address, ', ', Cities.city, ', ', States.state, ' ', ZipCodes.zip_code) AS Address
FROM Stores
INNER JOIN Addresses
ON Addresses.address_id = Stores.store_address
INNER JOIN Cities
ON Cities.city_id = Addresses.city
INNER JOIN States
ON States.state_id = Addresses.state
INNER JOIN ZipCodes
ON ZipCodes.zip_id = Addresses.zip_code;

-- add a new Store
INSERT INTO Stores (store_phone, store_email, store_address) VALUES
(:phoneInput, :emailInput, :address_from_store_address_form);

-- ####################################################################
-- The BROWSE products.html Page
-- ####################################################################

-- get all Products
SELECT Products.product_id AS ID, Products.product_description AS Description, ProductTypes.product_type AS Type, Products.product_price AS Price, ProductConditions.product_condition AS 'Condition'
FROM Products
INNER JOIN ProductTypes
ON ProductTypes.product_type_id = Products.product_type
INNER JOIN ProductConditions
ON ProductConditions.product_condition_id = Products.product_condition;

-- add a new Product
INSERT INTO Products (product_description, product_type, product_price, product_condition) VALUES
(:descriptionInput, :product_type_from_dropdown_Input, :priceInput, :product_condition_from_selection_Input);