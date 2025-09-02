import sqlite3
import sys
import os

from functools import reduce

class DB:
    # ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ Database (DB) Reader and Writer                                                                         │
    # │ 📒 Variables:                 Desc:                                                                     │
    # │    • conn                      sqlite3 object for managing transactions                                 │
    # │                                                                                                         │
    # │  ⚙️  Functions:                 Desc / Effects:                             Produces:                    │
    # │    • __init__(file, create)    Initialize with link to database file                                    │
    # │    • _lookForTable(identifier) Ensures table exists and returns name       "table1"                     │
    # │    • tables()                  Return list of tables as strings            ["table1", "table2", ... ]   │
    # │    • create(name, schema)      Create table with name, optional schema                                  │
    # │    • drop(identifier)          Drop table with matching name or indexing                                │
    # └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘



    # ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # ┃ __init__                                                                                                         ┃
    # ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    # │ Establishes connection to sqlite file. Raises ValueError if the file cannot be found.                            │
    # ├────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────┤
    # │ Input                  │ Description                                                                             │
    # │     • file (str)       │     The file path for the database to access                                            │
    # │     • create (bool)    │     If TRUE, the file will be created if it doesn't already exist                       │
    # └────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────┘
    def __init__(self, file, create = True):
        # Check input types
        if not isinstance(file, str):       raise TypeError(f"{file} should be a string")
        if not isinstance(create, bool):    raise TypeError(f"{create} should be a bool")

        if not bool(create) and not os.path.isfile(str(file)): raise ValueError(f"{file} does not exist")
        
        self.conn = sqlite3.connect(file, autocommit = True)

    

    # ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # ┃ _lookForTable                                                                                  [int, str] -> str ┃
    # ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    # │ Identifies the table by name or index and confirms the table exists. If the table exists, return the name of the │
    # │ table as a string. Otherwise, raise a ValueError.                                                                │
    # ├──────────────────┬─────────────────┬─────────────────────────────────────────────────────────────────────────────┤
    # │ Input            │ Type            │ Description                                                                 │
    # │   • identifier   │   • [str, int]  │   • If INT, check table by index of table list. If STR, check by name       │
    # └──────────────────┴─────────────────┴─────────────────────────────────────────────────────────────────────────────┘
    def _lookForTable(self, identifier):
        if not isinstance(identifier, (str, int)):   raise TypeError(f"{identifier} should be a string or int")
        def _doesNotExistError():                    raise ValueError(f"Table {identifier} does not exist")

        # Get current tables
        listOfTables = self.tables()
        
        # IF STR: Check existance directly
        if isinstance(identifier, str):
            if identifier not in listOfTables:
                _doesNotExistError()
            else:
                return identifier
        
        # IF INT: Handle indexing
        if isinstance(identifier, int):
            if identifier not in range(len(listOfTables)):  # Check if indexing by given number is possible
                _doesNotExistError()
            else:
                return listofTables[identifier]


    # ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # ┃ tables                                                                                      (None) -> tuple(str) ┃
    # ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    # │ Request table names from the sqlite connection. Returns a tuple of each table name as a string.                  │
    # └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    def tables(self):
        
        results = self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        names   = results.fetchall()
        
        # If the list is not empty, combine list of single-element tuples to one tuple
        if names: names = reduce(lambda a, b : a + b, names)
        
        return(names)
        
    # ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # ┃ create                                                                                        str, str -> (None) ┃
    # ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    # │ Add a new table to the sqlite file, and uses schema file if provided.                                            │
    # ├──────────────┬─────────┬─────────────────────────────────────────────────────────────────────────────────────────┤
    # │ Input        │ Type    │ Description                                                                             │
    # │   • name     │   • str │   • The name of the table to be created.                                                │
    # │   • schema   │   • str │   • (Optional) The file path of the schema to be used.                                  │
    # └──────────────┴─────────┴─────────────────────────────────────────────────────────────────────────────────────────┘
    def create(self, name, schema = None):
        # Check input types
        if not isinstance(name, str):                   raise TypeError(f"{name} should be a string")
        if not isinstance(schema, (str, type(None))):   raise TypeError(f"{schema} should be a string")
        if not os.path.isfile(schema):                  raise ValueError(f"{schema} does not exist")
        # Check name uniqueness
        if name in self.tables():                       raise ValueError(f"{name} should be unique in the database.")

        if(schema):
            file        = open(schema).read()                   # Read the file
            commands    = file.split(sep = ";")                 # If there are multiple commands, split them into separate strings
        else:
            commands    = [f"CREATE TABLE {name}();"]           # Command will create an empty table if no schema is provided

        for cmd in commands: self.conn.execute(cmd)             # Execute each command prepared above


    # ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # ┃ drop                                                                                        [int, str] -> (None) ┃
    # ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    # │ Removes identified table if it exists. No errors are raised if the table already does not exist.                 │
    # ├────────────────┬────────────────┬────────────────────────────────────────────────────────────────────────────────┤
    # │ Input          │ Type           │ Description                                                                    │
    # │   • identifier │   • [str, int] │   • If INT, check table by index of table list. If STR, check by name.         │
    # └────────────────┴────────────────┴────────────────────────────────────────────────────────────────────────────────┘
    def drop(self, identifier):
        # Check input types
        if not isinstance(identifier, (str, int)): raise TypeError(f"{identifier} should be a string or int")

        # Ensure existance before deleting
        try:
            identifier = self._lookForTable(identifier)
            # OK, delete table
            self.conn.execute(f"DROP TABLE {identifier}")
        except ValueError:
            pass
    # ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    # ┃ access                                                                                          [int, str] -> TB ┃
    # ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    # │ Return a TB (Table) object based on name or index.                                                               │
    # ├────────────────┬────────────────┬────────────────────────────────────────────────────────────────────────────────┤
    # │ Input          │ Type           │ Description                                                                    │
    # │   • identifier │   • [str, int] │   • If INT, check table by index of table list. If STR, check by name.         │
    # └────────────────┴────────────────┴────────────────────────────────────────────────────────────────────────────────┘
    def access(self, identifier):
        # Check input types
        if not isinstance(identifier, (str, int)): raise TypeError(f"{identifier} should be a string or int")

        # Ensure existance before initializing table object
        try:
            identifier = self._lookForTable(identifier)
            # OK, delete table
            return self.TB(self, identifier)
        except ValueError:
            pass

            
    """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ CLASS: TB (Table)                                                                                                ┃
    ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
    ┃ Encapsulates sqlite3 database transactions for a particular table in the database. It is intended to act as a    ┃
    ┃ child of a DB (database) object to:                                                                              ┃
    ┃   i.      Confirm the existence of the table when initializing.                                                  ┃
    ┃   ii.     Use the database connection object rather than opening a new, redundant connection.                    ┃
    ┣━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
    ┃ Functions:    ┃ Process:                                               ┃ Description:                            ┃
    ┣━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
    ┃   ⚙ __init__  │   ‣ DB, str                 -> TB                      │ Initialize parent and title variables.  ┃
    ┠───────────────┼────────────────────────────────────────────────────────┼─────────────────────────────────────────┨
    ┃   ⚙ headers   │   ‣ (None)                  -> tuple(str)              │ Get a list of the table headers.        ┃
    ┠───────────────┼────────────────────────────────────────────────────────┼─────────────────────────────────────────┨
    ┃   ⚙ select    │   ‣ str, str, bool          -> list(tuple[str, float]) │ Get rows, optional search terms.        ┃
    ┠───────────────┼────────────────────────────────────────────────────────┼─────────────────────────────────────────┨
    ┃   ⚙ insert    │   ‣ list(tuple[str, float]) -> (None)                  │ Insert row; strict data format needed.  ┃
    ┠───────────────┼────────────────────────────────────────────────────────┼─────────────────────────────────────────┨
    ┃   ⚙ delete    │   ‣ str, str                -> (None)                  │ Delete row(s) based on search term.     ┃
    ┗━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """
    class TB:
        # ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        # ┃ __init__                                                                                DB, [int, str] -> (None) ┃
        # ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        # │ Saves table name. Allows for sqlite3 data transactions between this table to be encapsulated by this object. If  │
        # │ the table does not exist, _lookForTable() raises a value error unhandled by this function.                       │
        # ├────────────────┬────────────────┬────────────────────────────────────────────────────────────────────────────────┤
        # │ Input          │ Type           │ Description                                                                    │
        # │   • database   │   • str        │   • The database file as a parent that holds the sqlite connection object.     │
        # │   • identifier │   • [str, int] │   • If INT, check table by index of table list. If STR, check by name.         │
        # └────────────────┴────────────────┴────────────────────────────────────────────────────────────────────────────────┘
        def __init__(self, database, identifier):
            # Check input types
            if not isinstance(identifier, (str, int)): raise TypeError(f"{identifier} should be a string or int")

            # Ensure existance of table
            self.title  = database._lookForTable(identifier)

            # OK, this object is good
            self.parent = database
            
        # -----------------------------------------------------------------------------------------
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # -----------------------------------------------------------------------------------------
        # Get a tuple of header names currently in the table
        # Return Types:
        #   • tuple of str
        def headers(self):
            results = self.parent.conn.execute(f"SELECT * FROM {self.title} LIMIT 0;")  # Get empty results, just need the headers
            headers = [label[0] for label in results.description]                       # Collect headers from description
            return  tuple(headers)
        # -----------------------------------------------------------------------------------------
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # -----------------------------------------------------------------------------------------
        # Runs the sqlite SELECT command. If no arguments are given, selects all. Returns rows as a list of tuples.
        # Parameters:
        #   • searchTerm        The item to look for in the searchColumn; all rows that have this term are returned
        #   • searchColumn      The column from which to look for the search term. Defaults to first column.
        #   • exact             Return only exact matches if True. Return similar matches otherwise.
        def select(self, searchTerm = None, searchColumn = None, exact = False):
            # Ensure search column exists
            if searchColumn and searchColumn not in self.headers(): raise ValueError(f"{searchColumn} is not a column")
        
            # Prepare command
            command = f"SELECT * FROM {self.title}"
            
            # If a search term was provided, narrow the results.
            if searchTerm:
                # -----------------------------------------------------
                if not searchColumn: searchColumn = self.headers()[0]
                # -----------------------------------------------------
                if exact:
                    command += f" WHERE {searchColumn} = {searchTerm}"
                else:
                    command += f" WHERE {searchColumn} LIKE '%{searchTerm}%'"
                # -----------------------------------------------------

            # OK, execute command and return results.
            return self.parent.conn.execute(command).fetchall()
        # -----------------------------------------------------------------------------------------
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # -----------------------------------------------------------------------------------------
        # Insert given data into the table. The data must be list of the same length as the headers.
        # Data must be a list of tuples
        # Parameters:
        #   • data (list)       List of tuples to insert at the bottom of the table  
        def insert(self, data):
            # For reference, get the number of headers.
            l = len(self.headers())

            # Ensure data is the same length
            if not len(data) == l: raise ValueError(f"{data} requires {l} arguments")
            
            # Create placeholder string for sqlite command
            placeholders = "(" + "?, " * (l - 1) + "?)"
            
            # Execute command
            self.parent.conn.execute(f"INSERT INTO {self.title} VALUES" + placeholders, data)
            self.parent.conn.commit()
        # -----------------------------------------------------------------------------------------
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # -----------------------------------------------------------------------------------------
        # Delete an entry in the table that matches the parameters given exactly
        # Parameters:
        #   • searchTerm        The item to look for in the searchColumn; all rows that have this term are returned
        #   • searchColumn      The column from which to look for the search term. Defaults to first column.
        def delete(self, searchTerm, searchColumn = None):
            # Get headers for reference
            headers = self.headers()
        
            # Ensure search column exists
            if searchColumn and searchColumn not in headers: raise ValueError(f"{searchColumn} is not a column")

            # Default to first column if needed
            if not searchColumn: searchColumn = headers[0]
            
            # Execute command
            self.parent.conn.execute(f"DELETE FROM {self.title} WHERE {searchColumn} = '{searchTerm}';")
