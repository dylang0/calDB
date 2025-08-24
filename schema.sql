CREATE TABLE entries (
	id 				INTEGER PRIMARY KEY AUTOINCREMENT,
	date 			TEXT,
	food 			TEXT,
	calories 		DOUBLE,
	carbohydrates 	DOUBLE,
	fats 			DOUBLE,
	protein 		DOUBLE,
	mass			DOUBLE,
	m_unit			TEXT
);

CREATE TABLE list (
	food			TEXT PRIMARY KEY,
	calories		DOUBLE,
	carbohydrates	DOUBLE,
	fats			DOUBLE,
	protein			DOUBLE,
	mass			DOUBLE,
	m_unit			TEXT
);
