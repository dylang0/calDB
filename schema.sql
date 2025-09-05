CREATE TABLE journal (
	id 				INTEGER PRIMARY KEY AUTOINCREMENT,
	date 			TEXT,
	food 			TEXT,
	calories 		DOUBLE,
	fats 			DOUBLE,
	carbohydrates 	DOUBLE,
	protein 		DOUBLE,
	weight			DOUBLE,
	volume			DOUBLE,
	vol_unit		TEXT
);

CREATE TABLE nutrition (
	food			TEXT PRIMARY KEY,
	calories		DOUBLE,
	fats			DOUBLE,
	carbohydrates	DOUBLE,
	protein			DOUBLE,
	weight			DOUBLE,
	volume			DOUBLE,
	vol_unit		TEXT
);
