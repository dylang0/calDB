CREATE TABLE journal (
	id 				INTEGER PRIMARY KEY AUTOINCREMENT,
	date 			TEXT,
	food 			TEXT,
	calories 		DOUBLE,
	carbohydrates 	DOUBLE,
	fats 			DOUBLE,
	protein 		DOUBLE,
	weight			DOUBLE,
	volume			DOUBLE,
	vol_unit		TEXT
);

CREATE TABLE nutrition (
	food			TEXT PRIMARY KEY,
	calories		DOUBLE,
	carbohydrates	DOUBLE,
	fats			DOUBLE,
	protein			DOUBLE,
	weight			DOUBLE,
	volume			DOUBLE,
	vol_unit		TEXT
);
