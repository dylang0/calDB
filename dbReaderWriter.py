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

            results = { header : () for header in self.headers }
            
            for row in data:
                for header, entry in zip(self.headers, row):
                    results[header] = results[header] + (entry,)
                
            return results
            
    # --------------------------------------------------
        def write(self, data):
            if not isinstance(data, dict): raise ValueError(data)
            


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
        # Catch incorrect input types
        if not isinstance(tableName, str):  raise TypeError(f"{tableName} must be a string")
        if not isinstance(headers, list):   raise TypeError(f"{headers} must be a list")

        # Convert headers to string for command input
        payload = ", ".join(headers)
        self._cur.execute(f"CREATE TABLE {tableName}({payload})")
        self._conn.commit()
    # --------------------------------------------------

    def schema(self, schemaFilePath):
        # Catch incorrect input types
        if not isinstance(schemaFilePath, str):
            raise TypeError(f"{schemaFilePath} must be a string")
        elif not os.path.isfile(schemaFilePath):
            raise ValueError(f"{schemaFilePath} does not exist")

        # File I/O
        file = open(schemaFilePath)
        schema = file.read()

        # Terminate at the first semicolon instance
        # Otherwise sqlite cannot execute schema commands
        termina = schema.find(";")                              # termina := -1 if ";" does not exist
        if not termina == -1: schema = schema[:termina + 1]     # cut schema command if termina exists

        # Execute schema commands
        self._cur.execute(schema)
        self._conn.commit()

    # --------------------------------------------------
    # Erase table where [ name == table if table is a str | table index == table if table is an int )
    def erase(self, table):
        existingTables = self.tables()
        # Handle input types
        if isinstance(table, int):
            try:
                table = existingTables[table]    # Get table at input index
            except IndexError:
                # Index already does not exist, no erasure needed
                return
            
    
        # Catch incorrect input types
        if not isinstance(table, (int, str)):
            raise TypeError(table)

        # Get table name as string by index if int was given
        elif isinstance(table, int):
            try:
                table = self.read[table]
            except IndexError:
                raise ValueError(table)
        try:
            self._cur.execute(f"DROP TABLE {table}")
            self._conn.commit()
        except sqlite3.OperationalError:
            # TPostcondition is already satisfied
            pass

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

    
        
