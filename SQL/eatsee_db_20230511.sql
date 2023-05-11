CREATE TABLE gender(
	gender_id  INT         GENERATED ALWAYS AS IDENTITY   PRIMARY KEY   NOT NULL,
	gender     varchar(10)
);

CREATE TABLE age(
	age_id     INT   GENERATED ALWAYS AS IDENTITY   PRIMARY KEY   NOT NULL,
	age_range  varchar(10)   NOT NULL
);

CREATE TABLE users (
	user_id       INT         GENERATED ALWAYS AS IDENTITY   PRIMARY KEY   NOT NULL,
	availability  BOOLEAN     NOT NULL,
	telename      VARCHAR(60) NOT NULL,
	age_ref_id    INT		  NOT NULL,
	gender_ref_id INT		  NOT NULL,
	CONSTRAINT fk_users_age
		FOREIGN KEY(age_ref_id)
			REFERENCES age(age_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
	CONSTRAINT fk_users_gender
		FOREIGN KEY(gender_ref_id)
			REFERENCES gender(gender_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);


CREATE TABLE age_ref(	
	user_ref_id   INT   NOT NULL,
	age_ref_id    INT   NOT NULL,
	CONSTRAINT fk_age
		FOREIGN KEY(user_ref_id)
			REFERENCES users(user_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(age_ref_id)
			REFERENCES age(age_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

CREATE TABLE gender_ref(
	user_ref_id    INT  NOT NULL,
	gender_ref_id  INT  NOT NULL,
	CONSTRAINT fk_gender
		FOREIGN KEY(user_ref_id)
			REFERENCES users(user_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(gender_ref_id)
			REFERENCES gender(gender_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE

);

CREATE TABLE chat(
	user_id     INT    NOT NULL,
	partner_id  INT    NOT NULL,
	CONSTRAINT fk_chat_user_users
		FOREIGN KEY(user_id)
			REFERENCES users(user_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
	CONSTRAINT fk_chat_partner_users
		FOREIGN KEY(partner_id)
			REFERENCES users(user_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

CREATE TABLE queue
(
	user_id    INT                         NOT NULL,
	timestamp  TIMESTAMP WITH TIME ZONE    NOT NULL,
	CONSTRAINT fk_queue_users
		FOREIGN KEY(user_id)
			REFERENCES users(user_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

CREATE TABLE cuisine(
	cuisine_id  INT     GENERATED ALWAYS AS IDENTITY   PRIMARY KEY   NOT NULL,
	cuisine     TEXT
);

CREATE TABLE cuisine_ref(
	user_ref_id     INT   NOT NULL,
	cuisine_ref_id  INT   NOT NULL,
	CONSTRAINT fk_cuisine
		FOREIGN KEY(user_ref_id)
			REFERENCES users(user_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(cuisine_ref_id)
			REFERENCES cuisine(cuisine_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

CREATE TABLE diet(
	diet_id         INT     GENERATED ALWAYS AS IDENTITY   PRIMARY KEY   NOT NULL,
	diet_res_type   TEXT
);

CREATE TABLE diet_ref(
	user_ref_id INT NOT NULL,
	diet_ref_id INT NOT NULL,
	CONSTRAINT fk_diet
		FOREIGN KEY(user_ref_id)
			REFERENCES users(user_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(diet_ref_id)
			REFERENCES diet(diet_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

CREATE TABLE restaurant(
	restaurant_id   INT            GENERATED ALWAYS AS IDENTITY   PRIMARY KEY   NOT NULL,
	restaurant_name varchar(100),
	url 	        TEXT
);

CREATE TABLE restaurant_location_ref(
	restaurant_ref_id  INT NOT NULL,
	area_ref_id		   INT NOT NULL,
	address			   TEXT,
	postal_code	   	   INT,
	CONSTRAINT fk_res_location_ref
		FOREIGN KEY(restaurant_ref_id)
			REFERENCES restaurant(restaurant_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(area_ref_id)
			REFERENCES area(area_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

CREATE TABLE restaurant_cuisine_ref(
	restaurant_ref_id           INT   NOT NULL,
	restaurant_cuisine_ref_id   INT   NOT NULL,
	CONSTRAINT fk_rescuisineref
		FOREIGN KEY(restaurant_ref_id)
			REFERENCES restaurant(restaurant_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(restaurant_cuisine_ref_id)
			REFERENCES cuisine(cuisine_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

CREATE TABLE restaurant_diet_ref(
	restaurant_ref_id       INT   NOT NULL,
	restaurant_diet_ref_id  INT   NOT NULL,
	CONSTRAINT fk_res_diet_ref
		FOREIGN KEY(restaurant_ref_id)
			REFERENCES restaurant(restaurant_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(restaurant_diet_ref_id)
			REFERENCES diet(diet_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);

CREATE TABLE area(
	area_id    INT   GENERATED ALWAYS AS IDENTITY   PRIMARY KEY   NOT NULL,
	area_name  TEXT   NOT NULL
);

CREATE TABLE region(
	region_id    INT   GENERATED ALWAYS AS IDENTITY   PRIMARY KEY   NOT NULL,
	region_name  TEXT   NOT NULL
);

CREATE TABLE area_region_ref(
	area_ref_id   INT NOT NULL,
	region_ref_id INT NOT NULL,
	CONSTRAINT fk_arearegionref
		FOREIGN KEY(area_ref_id)
			REFERENCES area(area_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY(region_ref_id)
			REFERENCES region(region_id)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);


/* 
Inserting Hard Coded Values into the DB
*/


INSERT INTO age (age_range)
VALUES ('16-19'), ('20-24'), ('25-29'),
('30-39'), ('40-49'), ('50 & Above');

INSERT INTO gender (gender)
VALUES ('Male'), ('Female'), ('Non Binary');

INSERT INTO cuisine (cuisine)
VALUES ('Chinese'), ('Malay'), ('Indian'), ('Western'), ('Korean'), ('Japanese'), ('Indonesian'), ('Vietnamese');

INSERT INTO diet (diet_res_type)
VALUES ('Halal'), ('Vegetarian'), ('Vegan');

INSERT INTO area (area_name)
VALUES ('Bishan'), ('Bukit Merah'), ('Bukit Timah'), ('Downtown Core'), ('Geylang'), ('Kallang'), ('Marina East'), ('Marina South'), ('Marine Parade'), ('Museum'), 
('Newton'), ('Novena'), ('Orchard'), ('Outram'), ('Queenstown'), ('River Valley'), ('Rochor'), ('Singapore River'), ('Southern Islands'), ('Straits View'), 
('Tanglin'), ('Toa Payoh'), ('Bedok'), ('Changi'), ('Changi Bay'), ('Pasir Ris'), ('Paya Lebar'), ('Tampines'), ('Central Water Catchment'), ('Lim Chu Kang'), 
('Mandai'), ('Sembawang'), ('Simpang'), ('Sungei Kadut'), ('Woodlands'), ('Yishun'), ('Ang Mo Kio'), ('Hougang'), ('North-Eastern Islands'), ('Punggol'), 
('Seletar'), ('Sengkang'), ('Serangoon'), ('Boon Lay'), ('Bukit Batok'), ('Bukit Panjang'), ('Choa Chu Kang'), ('Clementi'), ('Jurong East'), ('Jurong West'), 
('Pioneer'), ('Tengah'), ('Tuas'), ('Western Islands'), ('Western Water Catchment');

INSERT INTO region (region_name)
VALUES ('Central'), ('East'), ('North'), ('North-East'), ('West');

INSERT INTO area_region_ref (area_ref_id, region_ref_id)
VALUES (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1), (18, 1), (19, 1), (20, 1), 
(21, 1), (22, 1), (23, 2), (24, 2), (25, 2), (26, 2), (27, 2), (28, 2), (29, 3), (30, 3), (31, 3), (32, 3), (33, 3), (34, 3), (35, 3), (36, 3), (37, 4), (38, 4), (39, 4), 
(40, 4), (41, 4), (42, 4), (43, 4), (44, 5), (45, 5), (46, 5), (47, 5), (48, 5), (49, 5), (50, 5), (51, 5), (52, 5), (53, 5), (54, 5), (55, 5)