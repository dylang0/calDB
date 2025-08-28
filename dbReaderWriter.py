import sqlite3
import os

"""
dbReader wraps functions for accessing tables in sqlite3
databases. A dbReader object can be thought of as a
collection of abstract "Table" objects.
"""
class dbReaderWriter:
    """
    Inner Class: TableReaderWriter
    Wraps row reading (searching), writing, and erasing operations
    """
    # --------------------------------------------------
    
    class TableReaderWriter:
        def __init__(self, title, dbReaderWriter):
            self.title = title
            self._cur = dbReaderWriter._cur
            self._conn = dbReaderWriter._conn
            data = self._cur.execute(f"SELECT * FROM {self.title} LIMIT 0;")
            self.headers = tuple([tag[0] for tag in data.description])
    # --------------------------------------------------
        def read(self, searchTerm = None, col = None, exactMatch = False):
            if col == None:
                col = self.headers[0]

            if searchTerm:
                if exactMatch:
                    payload = f" WHERE {col} = '{searchTerm}';"
                else:
                    payload = f" WHERE {col} LIKE '%{searchTerm}%';"
            else:
                payload = ""

            data = self._cur.execute(f"SELECT * FROM {self.title}" + payload) # auto cursor.fetchall()

            results = { header: () for header in self.headers }
            
            for row in data:
                for header, entry in zip(self.headers, row):
                    results[header] = results[header] + (entry,)
                
            return results
    # --------------------------------------------------
        def write(self, data):
            if isinstance(data, dict):
                try:
                    data = [data[header] for header in self.headers]
                except KeyError:
                    raise ValueError(data)
            elif not isinstance(data, list):
                raise ValueError(data)

            for i in range(len(data)):
                if(isinstance(data[i], str)):
                    data[i] = "'" + data[i] + "'"
                if data[i] == None:
                    data[i] = "NULL"
                else:
                    data[i] = str(data[i])

            self._cur.execute(f"INSERT INTO {self.title} VALUES (" + ", ".join(data) + ")")
            self._conn.commit()
    # --------------------------------------------------
        def erase(self, searchTerm, col = None):
            if col == None:
                col = self.headers[0]
                
            if isinstance(searchTerm, str):
                searchTerm = "'" + searchTerm + "'"
                
            self._cur.execute(f"DELETE FROM {self.title} WHERE {col} = {searchTerm};")
            self._conn.commit()


    # --------------------------------------------------
    def __init__(self, dbFilePath, create = False):

        if not create and not os.path.isfile(dbFilePath):
            raise ValueError("database file does not exist.")
        
        self._conn = sqlite3.connect(dbFilePath)
        self._cur  = self._conn.cursor()

    # --------------------------------------------------
    def tables(self): # returns a tuple of table names as str
        tupleList = self._cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        return tuple([tableName[0] for tableName in tupleList])
        
    # --------------------------------------------------
    def write(self, tableName, headers):
        payload = ", ".join(headers)
        self._cur.execute(f"CREATE TABLE {tableName}({payload})")
        self._conn.commit()
    # --------------------------------------------------

    def schema(self, schemaFilePath):
        if not isinstance(schemaFilePath, str):
            raise ValueError("Schema file path is not a string")
        elif not os.path.isfile(schemaFilePath):
            raise ValueError("Provided schema file does not exist")
            
        file = open(schemaFilePath)
        schema = file.read()
        termina = schema.find(";") + 1
        schema = schema[:termina]
        self._cur.execute(schema)
        self._conn.commit()

    # --------------------------------------------------
    def erase(self, table):
        if not isinstance(table, (int, str)):
            raise TypeError(table)
        elif isinstance(table, int):
            try:
                table = self.read[table]
            except IndexError:
                raise ValueError(table)

        self._cur.execute(f"DROP TABLE {table}")
        self._conn.commit()

    # --------------------------------------------------
    def access(self, table):
        if not isinstance(table, (int, str)):
            raise TypeError(table)
        elif isinstance(table, int):
            try:
                table = self.read[table]
            except IndexError:
                raise ValueError(table)

        return self.TableReaderWriter(table, self)
    # --------------------------------------------------
    def __iter__(self):
        self.iterator = 0
        return self
        
    # --------------------------------------------------
    def __next__(self):
        try:
            name = self.tables()[self.iterator]
            self.iterator += 1
            return name
        except IndexError:
            raise StopIteration

    # --------------------------------------------------
    def __repr__(self):
        return "{ " + " ".join(self.tables()) + " }"

    
        
