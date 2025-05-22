------------------------------------------------------------------------------------------------------------------------------------------
DROP DATABASE IF EXISTS IFN582_GROUP84;

CREATE DATABASE IFN582_GROUP84;

USE IFN582_GROUP84;

-- CREATE-----------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE users (
userID INT AUTO_INCREMENT PRIMARY KEY,
userName VARCHAR(20) UNIQUE NOT NULL,
password VARCHAR(50) NOT NULL,
userType ENUM('Admin', 'User') NOT NULL,
createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE customers (
customerID INT AUTO_INCREMENT PRIMARY KEY,
userID INT NOT NULL,
firstName VARCHAR(50) NOT NULL,
surname VARCHAR(20) NOT NULL,
phoneNumber VARCHAR(15),
emailAddress VARCHAR(50) UNIQUE,
addressLine1 VARCHAR(50) NOT NULL,
addressLine2 VARCHAR(50) NOT NULL,
city VARCHAR(50) NOT NULL,
state VARCHAR(50) NOT NULL,
postCode VARCHAR(4) NOT NULL,
FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE suppliers (
supplierID INT AUTO_INCREMENT PRIMARY KEY,
supplierName VARCHAR(100) NOT NULL
);

CREATE TABLE category (
categoryCode VARCHAR(2) NOT NULL PRIMARY KEY,
categoryName VARCHAR(50) NOT NULL
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
imageURL VARCHAR(255),
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
orderNumber INT NOT NULL UNIQUE,
basketID INT NOT NULL,
customerID INT NOT NULL,
orderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
orderStatus ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Pending',
deliveryMethodCode ENUM('STANDARD', 'ECO', 'EXPRESS', 'TEMP') NOT NULL,
updatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY (basketID) REFERENCES baskets (basketID) ON DELETE CASCADE,
FOREIGN KEY (customerID) REFERENCES customers (customerID) ON DELETE CASCADE,
FOREIGN KEY (deliveryMethodCode) REFERENCES delivery_methods (deliveryMethodCode)
);

CREATE TABLE payments (
paymentID INT AUTO_INCREMENT PRIMARY KEY,
paymentNumber INT NOT NULL UNIQUE,
paymentMethod ENUM('Credit Card','Debit Card','After Pay'),
payeeName VARCHAR(50) NOT NULL,
paymentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
orderID INT NOT NULL,
customerID INT NOT NULL,
paymentStatus ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Pending',
createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY (orderID) REFERENCES orders (orderID) ON DELETE CASCADE,
FOREIGN KEY (customerID) REFERENCES customers (customerID) ON DELETE CASCADE
);

-- users
INSERT INTO users VALUES (NULL, 'SYSADMIN', '0000000000', 'Admin', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'NABILA', '0000000000', 'Admin', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'HANNAH', '0000000000', 'User', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'LUKE', '0000000000', 'User', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'ELSIE', '0000000000', 'User', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'MONICA', '0000000000', 'User', DEFAULT, DEFAULT);

-- customers
INSERT INTO customers VALUES (NULL, '3', 'Hannah', 'Law', '0432274880', 'N12229628@qut.edu.au', '2 George Street', 'Gardens Point', 'Brisbane', 'Queensland', '4000');
INSERT INTO customers VALUES (NULL, '4', 'Luke', 'Benjapattranon', NULL, 'N12258164@qut.edu.au', '2 George Street', 'Gardens Point', 'Brisbane', 'Queensland', '4000');
INSERT INTO customers VALUES (NULL, '5', 'Elsie', 'Shim', NULL, 'N12219151@qut.edu.au', '2 George Street', 'Gardens Point', 'Brisbane', 'Queensland', '4000');
INSERT INTO customers VALUES (NULL, '6', 'Monica', 'Nunes', NULL, 'N12240672@qut.edu.au', '2 George Street', 'Gardens Point', 'Brisbane', 'Queensland', '4000');

-- suppliers
INSERT INTO suppliers VALUES (NULL, 'Gardens Point Medical Inc.');
INSERT INTO suppliers VALUES (NULL, 'Kelvin Grove Medical Ltd.');

-- category
INSERT INTO category VALUES ('MD', 'Medicine');
INSERT INTO category VALUES ('MU', 'Makeup');
INSERT INTO category VALUES ('SC', 'Skincare');

-- items
INSERT INTO items VALUES ('38762059', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 10 pack', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 10 pack', NULL, NULL, '13.99', '9.50', '1', 'MD', '100', NULL);
INSERT INTO items VALUES ('13982406', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 80 pack', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 80 pack', NULL, NULL, '33.99', NULL, '1', 'MD', '100', NULL);
INSERT INTO items VALUES ('72145608', 'CeraVe Skin Renewing Night Cream 48g', 'CeraVe Skin Renewing Night Cream 48g', NULL, NULL, '41.50', '28.69', '2', 'SC', '100', NULL);
INSERT INTO items VALUES ('21458930', 'CeraVe Skin Renewing Night Cream 100g', 'CeraVe Skin Renewing Night Cream 100g', NULL, NULL, '79.99', NULL, '2', 'SC', '100', NULL);
INSERT INTO items VALUES ('26873194', 'CeraVe Moisturising Cream 170g', 'CeraVe Moisturising Cream 170g', NULL, NULL, '16.00', '11.19', '2', 'SC', '100', NULL);
INSERT INTO items VALUES ('36790128', 'CeraVe Moisturising Cream 454g', 'CeraVe Moisturising Cream 454g', NULL, NULL, '25.99', NULL, '2', 'SC', '100', NULL);
INSERT INTO items VALUES ('94018536', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Mint', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Mint', NULL, NULL, '11.99', '10.99', '1', 'MD', '100', NULL);
INSERT INTO items VALUES ('90871245', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Watermelon', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Watermelon', NULL, NULL, '11.99', '10.99', '1', 'MD', '100', NULL);
INSERT INTO items VALUES ('62846620', 'Maybelline Fit Me True-to-tone Blush - Rose', 'Maybelline Fit Me True-to-tone Blush - Rose', NULL, NULL, '9.49', '8.99', '2', 'MU', '100', NULL);
INSERT INTO items VALUES ('85623014', 'Maybelline Fit Me True-to-tone Blush - Coral', 'Maybelline Fit Me True-to-tone Blush - Coral', NULL, NULL, '9.49', '8.99', '2', 'MU', '100', NULL);
INSERT INTO items VALUES ('80439217', 'Maybelline Lasting Fix Setting Loose Powder', 'Maybelline Lasting Fix Setting Loose Powder', NULL, NULL, '9.99', '9.49', '2', 'MU', '100', NULL);
INSERT INTO items VALUES ('60381297', 'Maybelline Lasting Fix Loose Translucent Setting Powder', 'Maybelline Lasting Fix Loose Translucent Setting Powder', NULL, NULL, '9.99', NULL, '2', 'MU', '100', NULL);
INSERT INTO items VALUES ('17530942', 'Nurofen Zavance 96 Tablets', 'Nurofen Zavance 96 Tablets', NULL, NULL, '28.99', '20.99', '1', 'MD', '100', NULL);
INSERT INTO items VALUES ('74023185', 'Nurofen Zavance 96 Caplets', 'Nurofen Zavance 96 Caplets', NULL, NULL, '28.99', '20.99', '1', 'MD', '100', NULL);
INSERT INTO items VALUES ('58219437', 'Panadol Rapid 48 Caplets', 'Panadol Rapid 48 Caplets', NULL, NULL, '11.99', NULL, '1', 'MD', '100', NULL);
INSERT INTO items VALUES ('49217683', 'Panadol Rapid 48 Tablets', 'Panadol Rapid 48 Tablets', NULL, NULL, '8.99', NULL, '1', 'MD', '100', NULL);

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
INSERT INTO basket_items VALUES (NULL, 1, '94018536', 2);
INSERT INTO basket_items VALUES (NULL, 2, '80439217', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 2, '17530942', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 2, '58219437', 3);
INSERT INTO basket_items VALUES (NULL, 3, '74023185', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 3, '60381297', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 3, '49217683', DEFAULT);
INSERT INTO basket_items VALUES (NULL, 4, '72145608', DEFAULT);

-- orders
INSERT INTO orders VALUES (1, '1001', '3', '1', DEFAULT, DEFAULT, 'STANDARD', DEFAULT);
INSERT INTO orders VALUES (2, '1002', '1', '2', DEFAULT, DEFAULT, 'ECO', DEFAULT);
INSERT INTO orders VALUES (3, '1003', '4', '3', DEFAULT, DEFAULT, 'EXPRESS', DEFAULT);
INSERT INTO orders VALUES (4, '1004', '2', '4', DEFAULT, DEFAULT, 'TEMP', DEFAULT);

-- payments
INSERT INTO payments VALUES (NULL, '91001', 'Credit Card', 'Hannah Law', DEFAULT, '1', '1', DEFAULT, DEFAULT, DEFAULT);
INSERT INTO payments VALUES (NULL, '91002', 'Debit Card', 'Luke Benjapattranon', DEFAULT, '2', '2', DEFAULT, DEFAULT, DEFAULT);
INSERT INTO payments VALUES (NULL, '91003', 'After Pay', 'Elsie Shim', DEFAULT, '3', '3', DEFAULT, DEFAULT, DEFAULT);
INSERT INTO payments VALUES (NULL, '91004', 'After Pay', 'Monica Nunes', DEFAULT, '4', '4', DEFAULT, DEFAULT, DEFAULT);

-- READ------------------------------------------------------------------------------------------------------------------------------------
-- customers read table
SELECT
	customers.customerID AS 'Customer ID',
    users.userID AS 'User ID',
	users.userName AS 'User Name',
	CONCAT(customers.firstName, ' ', customers.surname) AS 'Customer Name',
    customers.phoneNumber AS 'Phone Number',
	customers.emailAddress AS 'Email Address',
	customers.addressLine1 AS 'Address Line 1',
	customers.addressLine2 AS 'Address Line 2',
	customers.city AS 'City',
	customers.state AS 'State',
	customers.postCode AS 'Post Code'
FROM customers
LEFT JOIN users ON customers.userID = users.userID
ORDER BY
	customers.customerID;

-- suppliers read table
SELECT
	supplierName AS 'Supplier Name'
FROM suppliers
ORDER BY
	supplierName;

-- category read table
SELECT
	categoryCode AS 'Category Code',
	categoryName AS 'Category Name'
FROM category
ORDER BY
	categoryCode;

-- users read table
SELECT
	users.userID AS 'User ID',
	users.userName AS 'User Name',
	customers.customerID AS 'Customer ID',
    CONCAT(customers.firstName, ' ', customers.surname) AS 'Customer Name',
	users.userType AS 'User Type',
	users.createdAt AS 'Creation Date & Time',
	users.updatedAt AS 'Updated Date & Time'
FROM users
LEFT JOIN customers ON customers.userID = users.userID
ORDER BY
	users.userID;

-- items read table
SELECT
	items.itemCode AS 'Item Code',
	items.itemName AS 'Item Name',
	items.itemDescription AS 'Item Description',
	items.itemLongDescription1 AS 'Instruction',
	items.itemLongDescription2 AS 'Ingredients',
	items.unitPrice AS 'Unit Price',
	IFNULL(items.discountPrice, items.unitPrice) AS 'Selling Price',
    category.categoryName AS 'Category Name',
    suppliers.supplierName AS 'Supplier Name',
	items.onhandQuantity AS 'Onhand Quantity',
	items.imageURL AS 'Image'
FROM items
LEFT JOIN 
	(category, suppliers) ON (category.categoryCode = items.categoryCode
    AND suppliers.supplierID = items.supplierID)
ORDER BY
	items.itemName;
	
-- baskets read table
SELECT
	baskets.basketID AS 'Basket ID',
    CONCAT(customers.firstName, ' ', customers.surname) AS 'Customer Name',
    basket_items.itemCode AS 'Item Code',
    items.itemName AS 'Item Name',
    SUM(basket_items.quantity) AS 'Quantity',
	IFNULL(items.discountPrice, items.unitPrice) AS 'Price',
    SUM(basket_items.quantity * IFNULL(items.discountPrice, items.unitPrice)) AS 'Total Amount'
FROM basket_items
JOIN
	(baskets, customers, items) ON (baskets.basketID = basket_items.basketID
	AND customers.customerID = baskets.customerID
	AND items.itemCode = basket_items.itemCode)
GROUP BY
	baskets.basketID,
    customers.firstName,
	customers.surname,
    basket_items.itemCode,
    items.itemName,
    items.discountPrice
ORDER BY 
	baskets.basketID;
	
-- orders read table
SELECT
	orders.orderID AS 'Order ID',
	orders.orderNumber AS 'Order Number',
	orders.orderDate AS 'Order Date & Time',
	orders.orderStatus AS 'Order Status',
    CONCAT(customers.firstName, ' ', customers.surname) AS 'Customer Name',
    COUNT(DISTINCT basket_items.itemCode) AS 'Item Count',
    SUM(basket_items.quantity) AS 'Order Quantity',
    SUM(basket_items.quantity * IFNULL(items.discountPrice, items.unitPrice)) AS 'Order Amount',
    delivery_methods.deliveryMethodName AS 'Delivery Method',
    delivery_methods.surchargePrice AS 'Delivery Fee',
	SUM(basket_items.quantity * IFNULL(items.discountPrice, items.unitPrice)) + delivery_methods.surchargePrice AS 'Order Total Amount',
	orders.updatedDate AS 'Updated Date & Time'
FROM orders
LEFT JOIN 
	(basket_items, customers, delivery_methods, items) ON (basket_items.basketID = orders.basketID
	AND customers.customerID = orders.customerID
	AND delivery_methods.deliveryMethodCode = orders.deliveryMethodCode
    AND items.itemCode = basket_items.itemCode)
GROUP BY
	orders.orderID,
    orders.orderNumber,
    orders.orderDate,
    orders.orderStatus,
    customers.firstName,
    customers.surname,
    delivery_methods.deliveryMethodName,
    delivery_methods.surchargePrice,
    orders.updatedDate
ORDER BY
	orders.orderID;
	
-- payments read table
SELECT
	payments.paymentNumber AS 'Payment Number',
	payments.paymentMethod AS 'Payment Method',
	payments.payeeName AS 'Payee Name',
	payments.paymentDate AS 'Payment Date & Time',
	orders.orderNumber AS 'Order Number',
	SUM(basket_items.quantity * IFNULL(items.discountPrice, items.unitPrice)) + delivery_methods.surchargePrice AS 'Payment Amount',
    CONCAT(customers.firstName, ' ', customers.surname) AS 'Customer Name',
	payments.paymentStatus AS 'Payment Status',
	payments.createdAt AS 'Creation Date & Time',
	payments.updatedAt AS 'Updated Date & Time'
FROM payments
JOIN 
	(orders, customers, basket_items, items, delivery_methods) ON (orders.orderID = payments.orderID
	AND customers.customerID = payments.customerID
    AND basket_items.basketID = orders.basketID
    AND items.itemCode = basket_items.itemCode
    AND delivery_methods.deliveryMethodCode = orders.deliveryMethodCode)
GROUP BY
    payments.paymentNumber,
    payments.paymentMethod,
    payments.payeeName,
    payments.paymentDate,
    orders.orderNumber,
    delivery_methods.surchargePrice,
    customers.firstName,
    customers.surname,
    payments.paymentStatus,
    payments.createdAt,
    payments.updatedAt
ORDER BY
	payments.paymentNumber;

-- UPDATE & DELETE-----------------------------------------------------------------------------------------------------------------------------------
-- (customers) add item into baskets
INSERT INTO basket_items (itemCode, quantity) VALUES (%s, %s);

-- (customers) adjust item quantity in baskets
UPDATE basket_items
SET quantity = %s
WHERE basketID = %s
AND itemCode = %s;

-- (customers) remove item from baskets
DELETE FROM basket_items
WHERE basketID = %s
AND itemCode = %s;

-- admin (items)
INSERT INTO items (itemCode, itemName, itemDescription, itemLongDescription1, itemLongDescription2, unitPrice, discountPrice, supplierID, categoryCode, onhandQuantity, imageURL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
UPDATE items SET unitPirce = %s, discountPrice = %s WHERE itemCode = %s;
DELETE FROM items WHERE itemCode = %s;

-- admin (category)
INSERT INTO category (categoryCode, categoryName) VALUES (%s, %s);
UPDATE category SET categoryCode = %s, categoryName = %s WHERE categoryCode = %s;
DELETE FROM category WHERE categoryCode = %s;

-- admin (orders)
INSERT INTO orders -- what should admin add into the order
UPDATE orders SET (orderStatus) VALUES (%s);
DELETE FROM orders WHERE orderNumber = %s;