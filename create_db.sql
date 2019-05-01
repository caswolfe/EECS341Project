/*
 * creates the necessary tables for the database
 */

/*
 * Select the database
 */
use team_12;

/*
 * Drop all pertinent tables to be relaced.
 */
DROP TABLE IF EXISTS transaction;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS user;

/*
 * User Table
 */
CREATE TABLE user(
	uid int(11) NOT NULL UNIQUE AUTO_INCREMENT,
	username varchar(40) NOT NULL UNIQUE,
	password varchar(40) NOT NULL,
	name varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	balance float NOT NULL,
	PRIMARY KEY (uid)
);

/*
 * Product Table
 */
CREATE TABLE product(
	pid int(11) NOT NULL UNIQUE AUTO_INCREMENT,
	sellerid int(11) NOT NULL,
	name varchar(255) NOT NULL,
	price float NOT NULL,
	quantity int(11) NOT NULL,
	PRIMARY KEY (pid),
	FOREIGN KEY (sellerid) references user(uid)
);

/*
 * Transaction Table
 */
CREATE TABLE transaction(
	tid int(11) NOT NULL UNIQUE AUTO_INCREMENT,
	pid int(11) NOT NULL,
	sellerid int(11) NOT NULL,
	buyerid int(11) NOT NULL,
	ts TIMESTAMP,
	quantity int(11) NOT NULL,
	ppunit float NOT NULL,
	PRIMARY KEY (pid, sellerid, buyerid, tid),
	FOREIGN KEY (pid) references product(pid),
	FOREIGN KEY (sellerid) references user(uid),
	FOREIGN KEY (buyerid) references user(uid)
);

/*
 * Chad
 */
INSERT INTO user (username, password, name, email, balance)
	VALUES ("chadswolfe", "password", "Chad Wolfe", "csw52@case.edu", 5900);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (1, "Saltine Crackers", 5.62, 4);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (1, "HDMI Cable", 8.99, 38);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (1, "Sunflower Seeds", 10.92, 3);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (1, "Bagel", 0.68, 17);

/*
 * Szabo
 */
INSERT INTO user (username, password, name, email, balance)
	VALUES ("andrewbszabo", "password", "Andrew Szabo", "abs93@case.edu", 2250);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (2, "A Litteral Human Hip", 750.99, 1);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (2, "Random Chemical Drum", 199.34, 2);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (2, "Medical Scalpel", 13.00, 14);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (2, "Thermal Camera", 257.72, 2);

/*
 * Duffy
 */
INSERT INTO user (username, password, name, email, balance)
	VALUES ("andrewjduffield", "password", "Andrew Duffield", "ajd173@case.edu", 5163146);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (3, "Blackout Curtains", 25.75, 15);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (3, "Gas Mask", 15.62, 8);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (3, "Canned Food", 8.27, 52);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (3, "Survivors Guide", 4.99, 3);

/*
 * Big Ben
 */
INSERT INTO user (username, password, name, email, balance)
	VALUES ("benjamingpierce", "password", "Benjamin Pierce", "bgp12@case.edu", 2);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (4, "Meal Swipe", 15.29, 14);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (4, "Leutner Ice Cream Tub", 17, 1);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (4, "Tuition Voucher", 44560.00, 2);

INSERT INTO product (sellerid, name, price, quantity)
	VALUES (4, "CWRU Street Sign", 14.72, 5);

/*
INSERT INTO product (sellerid, name, price, quantity)
	VALUES (, "", , );
*/

INSERT INTO transaction(pid, sellerid, buyerid, quantity, ppunit)
	VALUES (1, 1, 2, 1, 1.5);

INSERT INTO transaction(pid, sellerid, buyerid, quantity, ppunit)
	VALUES (5, 2, 1, 1, 2.5);

INSERT INTO transaction(pid, sellerid, buyerid, quantity, ppunit)
	VALUES (9, 3, 4, 3, 3.5);

INSERT INTO transaction(pid, sellerid, buyerid, quantity, ppunit)
	VALUES (16, 4, 3, 5, 4.5);

/*
INSERT INTO transaction(pid, sellerid, buyerid, quantity)
	VALUES (, , , );
*/
