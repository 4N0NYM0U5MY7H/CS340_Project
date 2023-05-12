-- Group 56: Dania Magana and August Frisk

SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- Customers Table
DROP TABLE IF EXISTS Customers;
CREATE TABLE Customers (
    customer_id int NOT NULL AUTO_INCREMENT,
    customer_name varchar(255) NOT NULL,
    customer_phone varchar(20) NOT NULL,
    customer_email varchar(255) NOT NULL,
    PRIMARY KEY (customer_id)
);

-- Example Data for Customers Table
INSERT INTO Customers (customer_name, customer_phone, customer_email) VALUES
('Ava Moreno', '(562) 201-9464', 'ava.moreno@example.com'),
('Oscar Mitchell', '(555) 330-8216', 'oscar.mitchell@example.com'),
('Daryl Caldwell', '(317) 476-7082', 'daryl.caldwell@example.com'),
('Lorraine Rogers', '(967) 508-1735', 'lorraine.rogers@example.com'),
('Ann Harris', '(246) 350-0973', 'ann.harris@example.com');

-- ProductConditions Table
DROP TABLE IF EXISTS ProductConditions;
CREATE TABLE ProductConditions (
    product_condition_id int NOT NULL AUTO_INCREMENT,
    product_condition varchar(50),
    PRIMARY KEY (product_condition_id)
);

-- Example Data for ProductConditions Table
INSERT INTO ProductConditions (product_condition) VALUES
('New'),
('Pre-Owned');

-- ProductTypes Table
DROP TABLE IF EXISTS ProductTypes;
CREATE TABLE ProductTypes (
    product_type_id int NOT NULL AUTO_INCREMENT,
    product_type varchar(255),
    PRIMARY KEY (product_type_id)
);

-- Example Data for ProductTypes Table
INSERT INTO ProductTypes (product_type) VALUES
('Console'),
('Video Game'),
('Toy'),
('Board Game'),
('Apparel');

-- Products Table
DROP TABLE IF EXISTS Products;
CREATE TABLE Products (
    product_id int NOT NULL AUTO_INCREMENT,
    product_description varchar(255) NOT NULL,
    product_type int,
    product_price decimal(19,2) NOT NULL,
    product_condition int,
    PRIMARY KEY (product_id),
    FOREIGN KEY (product_type) REFERENCES ProductTypes(product_type_id)
    ON DELETE CASCADE,
    FOREIGN KEY (product_condition) REFERENCES ProductConditions(product_condition_id)
    ON DELETE CASCADE
);

-- Example Data for Products Table
INSERT INTO Products (product_description, product_type, product_price, product_condition) VALUES
('PlayStation 5', (SELECT product_type_id FROM ProductTypes WHERE product_type = 'Console'), 499.99, (SELECT product_condition_id FROM ProductConditions WHERE product_condition = 'New')),
('Five Nights at Freddy''s Collectible Plush', (SELECT product_type_id FROM ProductTypes WHERE product_type = 'Toy'), 12.99, (SELECT product_condition_id FROM ProductConditions WHERE product_condition = 'Pre-Owned')),
('Super Mario Odyssey', (SELECT product_type_id FROM ProductTypes WHERE product_type = 'Video Game'), 54.99, (SELECT product_condition_id FROM ProductConditions WHERE product_condition = 'New'));

-- States Table
DROP TABLE IF EXISTS States;
CREATE TABLE States (
    state_id int NOT NULL AUTO_INCREMENT,
    state varchar(50) NOT NULL,
    PRIMARY KEY (state_id)
);

-- Example Data for States Table
INSERT INTO States (state) VALUES
('Oregon'),
('Ohio'),
('Montana');

-- Cities Table
DROP TABLE IF EXISTS Cities;
CREATE TABLE Cities (
    city_id int NOT NULL AUTO_INCREMENT,
    city varchar(100),
    PRIMARY KEY (city_id)
);

-- Example Data for Cities Table
INSERT INTO Cities (city) VALUES
('Corvallis'),
('Iowa Park'),
('Abilene');

-- ZipCodes Table
DROP TABLE IF EXISTS ZipCodes;
CREATE TABLE ZipCodes (
    zip_id int NOT NULL AUTO_INCREMENT,
    zip_code varchar(15),
    PRIMARY KEY (zip_id)
);

-- Example Data for ZipCodes Table
INSERT INTO ZipCodes (zip_code) VALUES
('97333'),
('39628'),
('64563');

-- Addresses Table
DROP TABLE IF EXISTS Addresses;
CREATE TABLE Addresses (
    address_id int NOT NULL AUTO_INCREMENT,
    street_address varchar(255) NOT NULL,
    state int,
    city int,
    zip_code int,
    PRIMARY KEY (address_id),
    FOREIGN KEY (state) REFERENCES States(state_id)
    ON DELETE CASCADE,
    FOREIGN KEY (city) REFERENCES Cities(city_id)
    ON DELETE CASCADE,
    FOREIGN KEY (zip_code) REFERENCES ZipCodes(zip_id)
    ON DELETE CASCADE
);

-- Example Data for Addresses Table
INSERT INTO Addresses (street_address, state, city, zip_code) VALUES
('5332 Walnut Hill Ln', (SELECT state_id FROM States WHERE state = 'Oregon'), (SELECT city_id FROM Cities WHERE city = 'Corvallis'), (SELECT zip_id FROM ZipCodes WHERE zip_code = '97333')),
('3798 Stevens Creek Blvd', (SELECT state_id FROM States WHERE state = 'Oregon'), (SELECT city_id FROM Cities WHERE city = 'Corvallis'), (SELECT zip_id FROM ZipCodes WHERE zip_code = '97333')),
('3445 Robinson Rd', (SELECT state_id FROM States WHERE state = 'Ohio'), (SELECT city_id FROM Cities WHERE city = 'Iowa Park'), (SELECT zip_id FROM ZipCodes WHERE zip_code = '39628')),
('5623 Spring St', (SELECT state_id FROM States WHERE state = 'Ohio'), (SELECT city_id FROM Cities WHERE city = 'Iowa Park'), (SELECT zip_id FROM ZipCodes WHERE zip_code = '39628')),
('7322 W Campbell Ave', (SELECT state_id FROM States WHERE state = 'Montana'), (SELECT city_id FROM Cities WHERE city = 'Abilene'), (SELECT zip_id FROM ZipCodes WHERE zip_code = '64563'));

-- Stores Table
DROP TABLE IF EXISTS Stores;
CREATE TABLE Stores (
    store_id int NOT NULL AUTO_INCREMENT,
    store_phone varchar(20) NOT NULL,
    store_email varchar(255) NOT NULL,
    store_address int,
    PRIMARY KEY (store_id),
    FOREIGN KEY (store_address) REFERENCES Addresses(address_id)
    ON DELETE CASCADE
);

-- Example Data for Stores Table
INSERT INTO Stores (store_phone, store_email, store_address) VALUES
('(268) 432-6210', 'heroelectronics1@email.com', (SELECT address_id FROM Addresses WHERE street_address = '5332 Walnut Hill Ln')),
('(679) 700-6746', 'heroelectronics2@email.com', (SELECT address_id FROM Addresses WHERE street_address = '3798 Stevens Creek Blvd')),
('(983) 821-8911', 'heroelectronics3@email.com', (SELECT address_id FROM Addresses WHERE street_address = '3445 Robinson Rd')),
('(385) 458-6153', 'heroelectronics4@email.com', (SELECT address_id FROM Addresses WHERE street_address = '5623 Spring St')),
('(642) 936-9797', 'heroelectronics5@email.com', (SELECT address_id FROM Addresses WHERE street_address = '7322 W Campbell Ave'));

-- SalesTaxes Table
DROP TABLE IF EXISTS SalesTaxes;
CREATE TABLE SalesTaxes (
    sales_tax_id int NOT NULL AUTO_INCREMENT,
    state int,
    sales_tax decimal(19,2) NOT NULL,
    PRIMARY KEY (sales_tax_id),
    FOREIGN KEY (state) REFERENCES States(state_id)
    ON DELETE CASCADE
);

-- Example Data for SalesTaxes Table
INSERT INTO SalesTaxes (state, sales_tax) VALUES
((SELECT state_id FROM States WHERE state = 'Oregon'), 0.00),
((SELECT state_id FROM States WHERE state = 'Ohio'), 5.75),
((SELECT state_id FROM States WHERE state = 'Montana'), 4.10);

-- Orders Table
DROP TABLE IF EXISTS Orders;
CREATE TABLE Orders (
    order_id int NOT NULL AUTO_INCREMENT,
    order_date date NOT NULL,
    customer_id int,
    store_id int,
    total_before_tax decimal(19,2) NOT NULL,
    sales_tax int,
    order_total decimal(19,2) NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    ON DELETE CASCADE,
    FOREIGN KEY (store_id) REFERENCES Stores(store_id)
    ON DELETE CASCADE,
    FOREIGN KEY (sales_tax) REFERENCES SalesTaxes(sales_tax_id)
    ON DELETE CASCADE
);

-- Example Data for Orders Table
INSERT INTO Orders (order_date, customer_id, store_id, total_before_tax, sales_tax, order_total) VALUES
('2023-05-01', (SELECT customer_id FROM Customers WHERE customer_name = 'Oscar Mitchell'), (SELECT store_id FROM Stores WHERE store_phone = '(983) 821-8911'), 499.99, (SELECT sales_tax_id FROM SalesTaxes WHERE state = (SELECT state_id FROM States WHERE state = 'Oregon')), 499.99),
('2023-04-28', (SELECT customer_id FROM Customers WHERE customer_name = 'Lorraine Rogers'), (SELECT store_id FROM Stores WHERE store_phone = '(679) 700-6746'), 25.98, (SELECT sales_tax_id FROM SalesTaxes WHERE state = (SELECT state_id FROM States WHERE state = 'Ohio')), 27.47),
('2023-04-27', (SELECT customer_id FROM Customers WHERE customer_name = 'Lorraine Rogers'), (SELECT store_id FROM Stores WHERE store_phone = '(679) 700-6746'), 54.99, (SELECT sales_tax_id FROM SalesTaxes WHERE state = (SELECT state_id FROM States WHERE state = 'Ohio')), 58.15);

-- StoreProducts Table
DROP TABLE IF EXISTS StoreProducts;
CREATE TABLE StoreProducts (
    store_product_id int NOT NULL AUTO_INCREMENT,
    store_id int,
    product_id int,
    number_in_stock int NOT NULL,
    PRIMARY KEY (store_product_id),
    FOREIGN KEY (store_id) REFERENCES Stores(store_id)
    ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
    ON DELETE CASCADE
);

-- Example Data for StoreProducts
INSERT INTO StoreProducts (store_id, product_id, number_in_stock) VALUES
((SELECT store_id FROM Stores WHERE store_phone = '(679) 700-6746'), (SELECT product_id FROM Products WHERE product_description = 'PlayStation 5'), 0),
((SELECT store_id FROM Stores WHERE store_phone = '(679) 700-6746'), (SELECT product_id FROM Products WHERE product_description = 'Five Nights at Freddy''s Collectible Plush'), 11),
((SELECT store_id FROM Stores WHERE store_phone = '(679) 700-6746'), (SELECT product_id FROM Products WHERE product_description = 'Super Mario Odyssey'), 10);

-- OrderDetails Table
DROP TABLE IF EXISTS OrderDetails;
CREATE TABLE OrderDetails (
    order_detail_id int NOT NULL AUTO_INCREMENT,
    order_id int,
    product_id int,
    order_quantity int NOT NULL,
    PRIMARY KEY (order_detail_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
    ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
    ON DELETE CASCADE
);

-- Example Data for OrderDetails Table
INSERT INTO OrderDetails (order_id, product_id, order_quantity) VALUES
(1, (SELECT product_id FROM Products WHERE product_description = 'PlayStation 5'), 1),
(2, (SELECT product_id FROM Products WHERE product_description = 'Five Nights at Freddy''s Collectible Plush'), 2),
(3, (SELECT product_id FROM Products WHERE product_description = 'Super Mario Odyssey'), 1);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;