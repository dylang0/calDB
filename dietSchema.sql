CREATE TABLE entries (
	id 				INTEGER PRIMARY KEY AUTOINCREMENT,
	date 			TEXT,
	food 			TEXT,
	calories 		INTEGER,
	carbohydrates 	INTEGER,
	fats 			INTEGER,
	protein 		INTEGER
);

CREATE TABLE foodList (
	food			TEXT PRIMARY KEY,
	calories		DOUBLE,
	weight_g		DOUBLE,
	carbohydrates	DOUBLE,
	fats			DOUBLE,
	protein			DOUBLE,
	vol_unit		TEXT,
	volume			DOUBLE
);
