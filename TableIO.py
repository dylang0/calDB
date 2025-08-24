import sqlite3
import os

class TableIO:
    def __init__(self, db, table):
        if not os.path.isfile(db): raise ValueError(f"{db} does not exist")
        self.db = db
        if not isinstance(db, str): pass
        self.table = table
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(f"SELECT * FROM {table} LIMIT 1")
        except sqlite3.OperationalError as e:
            raise ValueError(f"{table} does not exist in {db}")
        print(db)

    def search(self, target, col):
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE {col} LIKE ?", ("%" + target + "%",))
        return self.cursor.fetchall()

    def write(self, data, headers = ""):
        l = len(data)
        h = "(" + ", ".join(headers) + ")" if headers != "" else ""
        #print(h)
        #print(l)
        vals_placeholder = "( " + ("?, " * (l - 1)) + "? )"
        try:
            self.cursor.execute(f"INSERT INTO {self.table} {h} VALUES " + vals_placeholder, tuple(data))
            self.conn.commit()
            print(f"Wrote {data}")
        except sqlite3.OperationalError as error:
            print(error)

    def erase(self, target, col):
        try:
            self.cursor.execute(f"DELETE FROM {self.table} WHERE {col} = '{target}'")
            self.conn.commit()
        except sqlite3.OperationalError as error:
            print(error)

    def setTable(self, table):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.conn.commit()
        try:
            self.cursor.execute(f"SELECT * FROM {table} LIMIT 1")
            self.table = table
        except sqlite3.OperationalError as e:
            raise ValueError(f"{table} does not exist in {self.db}")
    
    def all(self):
        self.cursor.execute(f"SELECT * FROM {self.table}")
        return self.cursor.fetchall()
