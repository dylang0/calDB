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
	calories 		INTEGER,
	carbohydrates	INTEGER,
	fats			INTEGER,
	protein			INTEGER
);
