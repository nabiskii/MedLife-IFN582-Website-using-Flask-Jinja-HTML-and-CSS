DROP DATABASE IF EXISTS IFN582_GROUP84;

CREATE DATABASE IFN582_GROUP84;

USE IFN582_GROUP84;

CREATE TABLE customers (
customerID INT AUTO_INCREMENT PRIMARY KEY,
firstName VARCHAR(50) NOT NULL,
surname VARCHAR(20) NOT NULL,
phoneNumber VARCHAR(15),
emailAddress VARCHAR(50) UNIQUE,
addressLine1 VARCHAR(50) NOT NULL,
addressLine2 VARCHAR(50) NOT NULL,
city VARCHAR(50) NOT NULL,
state VARCHAR(50) NOT NULL,
postCode VARCHAR(4) NOT NULL
);

CREATE TABLE suppliers (
supplierID INT AUTO_INCREMENT PRIMARY KEY,
supplierName VARCHAR(100) NOT NULL
);

CREATE TABLE category (
categoryCode VARCHAR(2) NOT NULL PRIMARY KEY,
categoryName VARCHAR(50) NOT NULL
);

CREATE TABLE users (
userID INT AUTO_INCREMENT PRIMARY KEY,
userName VARCHAR(20) UNIQUE NOT NULL,
customerID INT,
password VARCHAR(50) NOT NULL,
userType ENUM('Admin', 'User') NOT NULL,
createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY (customerID) REFERENCES customers (customerID)
);

CREATE TABLE items (
itemCode VARCHAR(10) PRIMARY KEY,
itemName VARCHAR(100) NOT NULL,
itemDescription VARCHAR(250) NOT NULL,
itemLongDescription1 TEXT,
itemLongDescription2 TEXT,
unitPrice DECIMAL(10,2) NOT NULL,
discountPrice DECIMAL(10,2),
CHECK (discountPrice IS NULL OR discountPrice <= unitPrice),
supplierID INT NOT NULL,
categoryCode VARCHAR(2) NOT NULL,
onhandQuantity INT NOT NULL,
FOREIGN KEY (categoryCode) REFERENCES category (categoryCode),
FOREIGN KEY (supplierID) REFERENCES suppliers (supplierID)
);

CREATE TABLE baskets (
basketID INT AUTO_INCREMENT PRIMARY KEY,
customerID INT NOT NULL,
FOREIGN KEY (customerID) REFERENCES customers (customerID) ON DELETE CASCADE
);

CREATE TABLE basket_items (
basketItemID INT AUTO_INCREMENT PRIMARY KEY,
basketID INT NOT NULL,
itemCode VARCHAR(10) NOT NULL,
quantity INT DEFAULT 1,
CHECK (quantity > 0),
FOREIGN KEY (basketID) REFERENCES baskets (basketID) ON DELETE CASCADE,
FOREIGN KEY (itemCode) REFERENCES items (itemCode)
);

CREATE TABLE delivery_methods (
deliveryMethodCode ENUM('STANDARD', 'ECO', 'EXPRESS', 'TEMP') PRIMARY KEY,
deliveryMethodName VARCHAR (50) NOT NULL,
surchargePrice DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
orderID INT AUTO_INCREMENT PRIMARY KEY,
orderNumber INT NOT NULL,
basketID INT NOT NULL,
customerID INT NOT NULL,
orderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
order_status ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Pending',
deliveryMethodCode ENUM('STANDARD', 'ECO', 'EXPRESS', 'TEMP') NOT NULL,
updatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY (basketID) REFERENCES baskets (basketID) ON DELETE CASCADE,
FOREIGN KEY (customerID) REFERENCES customers (customerID) ON DELETE CASCADE,
FOREIGN KEY (deliveryMethodCode) REFERENCES delivery_methods (deliveryMethodCode)
);

CREATE TABLE payments (
paymentID INT AUTO_INCREMENT PRIMARY KEY,
paymentNumber INT NOT NULL,
paymentMethod ENUM('Credit Card','Debit Card','After Pay'),
payeeName VARCHAR(50) NOT NULL,
paymentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
orderID INT NOT NULL,
customerID INT NOT NULL,
createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY (orderID) REFERENCES orders (orderID) ON DELETE CASCADE,
FOREIGN KEY (customerID) REFERENCES customers (customerID) ON DELETE CASCADE
);

-- Customers
INSERT INTO customers VALUES (NULL, 'Hannah', 'Law', '0432274880', 'N12229628@qut.edu.au', '2 George Street', 'Gardens Point', 'Brisbane', 'Queensland', '4000');
INSERT INTO customers VALUES (NULL, 'Luke', 'Benjapattranon', NULL, 'N12258164@qut.edu.au', '2 George Street', 'Gardens Point', 'Brisbane', 'Queensland', '4000');
INSERT INTO customers VALUES (NULL, 'Elsie', 'Shim', NULL, 'N12219151@qut.edu.au', '2 George Street', 'Gardens Point', 'Brisbane', 'Queensland', '4000');
INSERT INTO customers VALUES (NULL, 'Monica', 'Nunes', NULL, 'N12240672@qut.edu.au', '2 George Street', 'Gardens Point', 'Brisbane', 'Queensland', '4000');

-- Users
REPLACE INTO users VALUES (NULL, 'SYSADMIN', NULL, '0000000000', 'Admin', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'NABILA', NULL, '0000000000', 'Admin', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'HANNAH', '1', '0000000000', 'User', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'LUKE', '2', '0000000000', 'User', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'ELSIE','3', '0000000000', 'User', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'MONICA', '4', '0000000000', 'User', DEFAULT, DEFAULT);

-- suppliers
INSERT INTO suppliers VALUES (NULL, 'Gardens Point Medical Inc.');
INSERT INTO suppliers VALUES (NULL, 'Kelvin Grove Medical Ltd.');

-- category
INSERT INTO category VALUES ('MD', 'Medicine');
INSERT INTO category VALUES ('MU', 'Makeup');
INSERT INTO category VALUES ('SC', 'Skincare');

-- items
INSERT INTO items VALUES ('38762059', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 10 pack', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 10 pack', NULL, NULL, '13.99', '9.50', '1', 'MD', '100');
INSERT INTO items VALUES ('13982406', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 80 pack', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 80 pack', NULL, NULL, '33.99', NULL, '1', 'MD', '100');
INSERT INTO items VALUES ('72145608', 'CeraVe Skin Renewing Night Cream 48g', 'CeraVe Skin Renewing Night Cream 48g', NULL, NULL, '41.50', '28.69', '2', 'SC', '100');
INSERT INTO items VALUES ('21458930', 'CeraVe Skin Renewing Night Cream 100g', 'CeraVe Skin Renewing Night Cream 100g', NULL, NULL, '79.99', NULL, '2', 'SC', '100');
INSERT INTO items VALUES ('26873194', 'CeraVe Moisturising Cream 170g', 'CeraVe Moisturising Cream 170g', NULL, NULL, '16.00', '11.19', '2', 'SC', '100');
INSERT INTO items VALUES ('36790128', 'CeraVe Moisturising Cream 454g', 'CeraVe Moisturising Cream 454g', NULL, NULL, '25.99', NULL, '2', 'SC', '100');
INSERT INTO items VALUES ('94018536', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Mint', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Mint', NULL, NULL, '11.99', '10.99', '1', 'MD', '100');
INSERT INTO items VALUES ('90871245', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Watermelon', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Watermelon', NULL, NULL, '11.99', '10.99', '1', 'MD', '100');
INSERT INTO items VALUES ('62846620', 'Maybelline Fit Me True-to-tone Blush - Rose', 'Maybelline Fit Me True-to-tone Blush - Rose', NULL, NULL, '9.49', '8.99', '2', 'MU', '100');
INSERT INTO items VALUES ('85623014', 'Maybelline Fit Me True-to-tone Blush - Coral', 'Maybelline Fit Me True-to-tone Blush - Coral', NULL, NULL, '9.49', '8.99', '2', 'MU', '100');
INSERT INTO items VALUES ('80439217', 'Maybelline Lasting Fix Setting Loose Powder', 'Maybelline Lasting Fix Setting Loose Powder', NULL, NULL, '9.99', '9.49', '2', 'MU', '100');
INSERT INTO items VALUES ('60381297', 'Maybelline Lasting Fix Loose Translucent Setting Powder', 'Maybelline Lasting Fix Loose Translucent Setting Powder', NULL, NULL, '9.99', NULL, '2', 'MU', '100');
INSERT INTO items VALUES ('17530942', 'Nurofen Zavance 96 Tablets', 'Nurofen Zavance 96 Tablets', NULL, NULL, '28.99', '20.99', '1', 'MD', '100');
INSERT INTO items VALUES ('74023185', 'Nurofen Zavance 96 Caplets', 'Nurofen Zavance 96 Caplets', NULL, NULL, '28.99', '20.99', '1', 'MD', '100');
INSERT INTO items VALUES ('58219437', 'Panadol Rapid 48 Caplets', 'Panadol Rapid 48 Caplets', NULL, NULL, '11.99', NULL, '1', 'MD', '100');
INSERT INTO items VALUES ('49217683', 'Panadol Rapid 48 Tablets', 'Panadol Rapid 48 Tablets', NULL, NULL, '8.99', NULL, '1', 'MD', '100');

-- delivery_methods
INSERT INTO delivery_methods VALUES ('STANDARD', 'Standard Delivery', '5.00');
INSERT INTO delivery_methods VALUES ('ECO', 'Eco-Friendly Delivery', '8.00');
INSERT INTO delivery_methods VALUES ('EXPRESS', 'Express Delivery', '15.00');
INSERT INTO delivery_methods VALUES ('TEMP', 'Temperature-Controlled Delivery', '25.00');

-- baskets
INSERT INTO baskets VALUES (NULL, '2');
INSERT INTO baskets VALUES (NULL, '4');
INSERT INTO baskets VALUES (NULL, '1');
INSERT INTO baskets VALUES (NULL, '3');

-- basket_items
INSERT INTO basket_items VALUES (NULL, 1, '13982406', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 1, '94018536', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 2, '80439217', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 2, '17530942', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 2, '58219437', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 3, '74023185', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 3, '60381297', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 3, '49217683', DEFAULT);

-- orders
INSERT INTO orders VALUES (NULL, '1001', '1', '1', DEFAULT, DEFAULT, 'STANDARD', DEFAULT);
INSERT INTO orders VALUES (NULL, '1002', '2', '3', DEFAULT, DEFAULT, 'ECO', DEFAULT);
INSERT INTO orders VALUES (NULL, '1003', '3', '4', DEFAULT, DEFAULT, 'EXPRESS', DEFAULT);
INSERT INTO orders VALUES (NULL, '1004', '4', '2', DEFAULT, DEFAULT, 'TEMP', DEFAULT);

-- payments
INSERT INTO payments VALUES (NULL, '91001', 'Credit Card', 'Hannah Law', DEFAULT, '1', '1', DEFAULT, DEFAULT);
INSERT INTO payments VALUES (NULL, '91002', 'Debit Card', 'Monica Nunes', DEFAULT, '2', '4', DEFAULT, DEFAULT);
INSERT INTO payments VALUES (NULL, '91003', 'After Pay', 'Elsie Shim', DEFAULT, '3', '3', DEFAULT, DEFAULT);
INSERT INTO payments VALUES (NULL, '91003', 'After Pay', 'Luke Benjapattranon', DEFAULT, '4', '2', DEFAULT, DEFAULT);