CREATE TABLE entries (
	id 				INTEGER PRIMARY KEY AUTOINCREMENT,
	date 			TEXT,
	food 			TEXT,
	calories 		DOUBLE,
	carbohydrates 	DOUBLE,
	fats 			DOUBLE,
	protein 		DOUBLE,
	weight_g		DOUBLE,
	volume			DOUBLE,
	vol_unit		TEXT
);

CREATE TABLE foodList (
	food			TEXT PRIMARY KEY,
	calories		DOUBLE,
	carbohydrates	DOUBLE,
	fats			DOUBLE,
	protein			DOUBLE,
	weight_g		DOUBLE,
	volume			DOUBLE,
	vol_unit		TEXT
);
