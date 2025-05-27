------------------------------------------------------------------------------------------------------------------------------------------
DROP DATABASE IF EXISTS IFN582_GROUP84;

CREATE DATABASE IFN582_GROUP84;

USE IFN582_GROUP84;

-- CREATE-----------------------------------------------------------------------------------------------------------------------------------
-- updated on 23 May 2025
CREATE TABLE users (
userID INT AUTO_INCREMENT PRIMARY KEY,
userName VARCHAR(20) UNIQUE NOT NULL,
password VARCHAR(80) NOT NULL,
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

CREATE TABLE delivery_methods (
deliveryMethodCode ENUM('STANDARD', 'ECO', 'EXPRESS', 'TEMP') PRIMARY KEY,
deliveryMethodName VARCHAR (50) NOT NULL,
surchargePrice DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
orderID INT AUTO_INCREMENT PRIMARY KEY,
customerID INT NOT NULL,
orderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
orderStatus ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Pending',
deliveryMethodCode ENUM('STANDARD', 'ECO', 'EXPRESS', 'TEMP') NOT NULL,
orderTotalAmount DECIMAL(10,2) NOT NULL,
updatedDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
FOREIGN KEY (customerID) REFERENCES customers (customerID) ON DELETE CASCADE,
FOREIGN KEY (deliveryMethodCode) REFERENCES delivery_methods (deliveryMethodCode)
);

CREATE TABLE subscription (
subscriptionID INT AUTO_INCREMENT PRIMARY KEY,
emailAddress VARCHAR(50) NOT NULL,
createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- users (Default password = test1234)
INSERT INTO users VALUES (NULL, 'SYSADMIN', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'Admin', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'NABILA', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'Admin', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'HANNAH', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'User', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'LUKE', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'User', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'ELSIE', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'User', DEFAULT, DEFAULT);
INSERT INTO users VALUES (NULL, 'MONICA', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'User', DEFAULT, DEFAULT);

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
INSERT INTO items VALUES ('38762059', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 10 pack', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 10 pack', 'Claratyne Hayfever Allergy Relief tablets are non-drowsy and provide rapid 24 hour relief from the symptoms of hayfever allergy.', 'Always read the label and follow the directions for use.', '13.99', '9.50', '1', 'MD', '100', '38762059.jpg');
INSERT INTO items VALUES ('13982406', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 80 pack', 'Claratyne Allergy & Hayfever Relief Antihistamine Tablets 80 pack', 'Claratyne Hayfever Allergy Relief tablets are non-drowsy and provide rapid 24 hour relief from the symptoms of hayfever allergy.', 'Always read the label and follow the directions for use.', '33.99', NULL, '1', 'MD', '100', '13982406.jpg');
INSERT INTO items VALUES ('72145608', 'CeraVe Skin Renewing Night Cream 48g', 'CeraVe Skin Renewing Night Cream 48g', 'Skin renewing night cream with peptides', 'Apply the CeraVe Skin Renewing Night Cream to freshly cleansed face in small dots around your face. Gently massage the night cream into the skin until thoroughly absorbed. Use it every night before bed in your evening skincare routine.', '41.50', '28.69', '2', 'SC', '100', '72145608.jpg');
INSERT INTO items VALUES ('21458930', 'CeraVe Skin Renewing Night Cream 100g', 'CeraVe Skin Renewing Night Cream 100g', 'Skin renewing night cream with peptides', 'Apply the CeraVe Skin Renewing Night Cream to freshly cleansed face in small dots around your face. Gently massage the night cream into the skin until thoroughly absorbed. Use it every night before bed in your evening skincare routine.', '79.99', NULL, '2', 'SC', '100', '21458930.jpg');
INSERT INTO items VALUES ('26873194', 'CeraVe Moisturising Cream 170g', 'CeraVe Moisturising Cream 170g', 'Rich Ceramide moistering cream for dry to very dry skin.', 'Apply liberally as often as needed, or as directed by a physician.', '16.00', '11.19', '2', 'SC', '100', '26873194.jpg');
INSERT INTO items VALUES ('36790128', 'CeraVe Moisturising Cream 454g', 'CeraVe Moisturising Cream 454g', 'Rich Ceramide moistering cream for dry to very dry skin.', 'Apply liberally as often as needed, or as directed by a physician.', '25.99', NULL, '2', 'SC', '100', '36790128.jpg');
INSERT INTO items VALUES ('94018536', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Mint', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Mint', 'Difflam Plus Anaesthetic Sore Throat Spray has a triple action antibacterial + anti-inflammatory + anaesthetic formula for fast numbing relief of a sore throat.', 'Spray 3 times directly onto the sore/inflamed area Swallow gently. Before first use or after a period of non-use, prime the spray by depressing the pump until the mist is released. After use, wipe the nozzle with a tissue to prevent blockage.', '11.99', '10.99', '1', 'MD', '100', '94018536.jpg');
INSERT INTO items VALUES ('90871245', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Watermelon', 'Difflam Plus Sore Throat Anaesthetic Spray 30ml - Watermelon', 'Difflam Plus Anaesthetic Sore Throat Spray has a triple action antibacterial + anti-inflammatory + anaesthetic formula for fast numbing relief of a sore throat.', 'Spray 3 times directly onto the sore/inflamed area Swallow gently. Before first use or after a period of non-use, prime the spray by depressing the pump until the mist is released. After use, wipe the nozzle with a tissue to prevent blockage.', '11.99', '10.99', '1', 'MD', '100', '90871245.jpg');
INSERT INTO items VALUES ('62846620', 'Maybelline Fit Me True-to-tone Blush - Rose', 'Maybelline Fit Me True-to-tone Blush - Rose', 'Create a natural flush of colour with Maybelline Fit Me Blush.', 'Sweep blush onto the apples of the cheeks from the cheekbones to temples.', '9.49', '8.99', '2', 'MU', '100', '62846620.jpg');
INSERT INTO items VALUES ('85623014', 'Maybelline Fit Me True-to-tone Blush - Coral', 'Maybelline Fit Me True-to-tone Blush - Coral', 'Create a natural flush of colour with Maybelline Fit Me Blush.', 'Sweep blush onto the apples of the cheeks from the cheekbones to temples.', '9.49', '8.99', '2', 'MU', '100', '85623014.jpg');
INSERT INTO items VALUES ('80439217', 'Maybelline Lasting Fix Setting Loose Powder', 'Maybelline Lasting Fix Setting Loose Powder', "Maybelline's loose powder that sets foundation and perfects the look of skin for an airbrush effect. Maybelline Master Fix Translucent Loose Powder is a micro-fine loose powder that sets makeup, mattifies and blurs for an invisible finish with a soft-focus effect.", 'Swirl lightly over face with a powder brush. Can be used alone or on top of makeup.', '9.99', '9.49', '2', 'MU', '100', '80439217.jpg');
INSERT INTO items VALUES ('60381297', 'Maybelline Lasting Fix Loose Translucent Setting Powder', 'Maybelline Lasting Fix Loose Translucent Setting Powder', "Maybelline's loose powder that sets foundation and perfects the look of skin for an airbrush effect. Maybelline Master Fix Translucent Loose Powder is a micro-fine loose powder that sets makeup, mattifies and blurs for an invisible finish with a soft-focus effect.", 'Swirl lightly over face with a powder brush. Can be used alone or on top of makeup.', '9.99', NULL, '2', 'MU', '100', '60381297.jpg');
INSERT INTO items VALUES ('17530942', 'Nurofen Zavance 96 Tablets', 'Nurofen Zavance 96 Tablets', 'Nurofen Zavance is absorbed up to 2X faster than standard Nurofen. They are easy to swallow and are fast and effective in the temporary relief of pain and/or inflammation associated with: headache, migraine headache, tension headache, muscular pain, cold & flu symptoms, period pain, dental pain, sinus pain, back pain, arthritic pain, Reduces fever.', 'Suitable For: Adults and children from 7 years. For the temporary relief of pain and/or inflammation.', '28.99', '20.99', '1', 'MD', '100', '17530942.jpg');
INSERT INTO items VALUES ('74023185', 'Nurofen Zavance 96 Caplets', 'Nurofen Zavance 96 Caplets', 'Nurofen Zavance is absorbed up to 2X faster than standard Nurofen. They are easy to swallow and are fast and effective in the temporary relief of pain and/or inflammation associated with: headache, migraine headache, tension headache, muscular pain, cold & flu symptoms, period pain, dental pain, sinus pain, back pain, arthritic pain, Reduces fever.', 'Suitable For: Adults and children from 7 years. For the temporary relief of pain and/or inflammation.', '28.99', '20.99', '1', 'MD', '100', '74023185.jpg');
INSERT INTO items VALUES ('58219437', 'Panadol Rapid 48 Caplets', 'Panadol Rapid 48 Caplets', 'Panadol Rapid Paracetamol 500mg is a fast, effective temporary relief of pain and discomfort associated with Headache/Tension headache, Migraine headache, Muscular aches, Period pain, Toothache, Cold & flu symptoms. Reduces fever.', '2 Caplets in every 4-6 hrs with water as required (maximum 8 caplets in 24 hrs)', '11.99', NULL, '1', 'MD', '100', '58219437.jpg');
INSERT INTO items VALUES ('49217683', 'Panadol Rapid 48 Tablets', 'Panadol Rapid 48 Tablets', 'Panadol Rapid Paracetamol 500mg is a fast, effective temporary relief of pain and discomfort associated with Headache/Tension headache, Migraine headache, Muscular aches, Period pain, Toothache, Cold & flu symptoms. Reduces fever.', '2 Tablets in every 4-6 hrs with water as required (maximum 8 caplets in 24 hrs)', '8.99', NULL, '1', 'MD', '100', '49217683.jpg');

-- delivery_methods
INSERT INTO delivery_methods VALUES ('STANDARD', 'Standard Delivery', '5.00');
INSERT INTO delivery_methods VALUES ('ECO', 'Eco-Friendly Delivery', '8.00');
INSERT INTO delivery_methods VALUES ('EXPRESS', 'Express Delivery', '15.00');
INSERT INTO delivery_methods VALUES ('TEMP', 'Temperature-Controlled Delivery', '25.00');


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