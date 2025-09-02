import DB
import sys
import os

from sqlite3    import IntegrityError
from foodstruct import Food
from datetime   import date
from tabulate   import tabulate

"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚙ rowToFood                                                                            tuple[str, float] -> Food ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Converts row results from table selection into a food object type.                                               ┃
┣━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Parameters  ┃ Type                     ┃ Description                                                             ┃
┣━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃   data      │  tuple[str, float]       │ Table data (row) to convert.                                            ┃
┗━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
def rowToFood(data):
    print(data)
    f = Food(str(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4]), 
                 float(data[5]), float(data[6]), str(data[7]))
    return f
    


"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚙ showTable                                                 list(tuple[str, float]) -> [tuple[str, float], None] ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Tabulates row data and optionally prompts the user for selection, returning the element from the list. Returns   ┃
┃ None if selection is invalid.                                                                                    ┃
┣━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Parameters  ┃ Type                     ┃ Description                                                             ┃
┣━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃   data      │  list(tuple[str, float]) │ Table data from sqlite3 "SELECT" command. Tabulated and prompted for    ┃
┃             │                          │ selection.                                                              ┃
┠─────────────┼──────────────────────────┼─────────────────────────────────────────────────────────────────────────┨
┃   headers   │  [str, list(str)]        │ Headers to use in the table displayed to the user. Blank by default.    ┃
┠─────────────┼──────────────────────────┼─────────────────────────────────────────────────────────────────────────┨
┃   hideFirst │  bool                    │ If TRUE, do not display the first column. FALSE by default.             ┃
┠─────────────┼──────────────────────────┼─────────────────────────────────────────────────────────────────────────┨
┃   select    │  bool                    │ If TRUE, prompt user for input.                                         ┃
┗━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
def showTable(data, headers = "", hideFirst = False, select = True):
    # Add index column. User selects based on this index.
    l = len(data)
    if l == 0: return None

    # Create a version of the data that has these indices
    concatenatedData = []
    for i in range(l): 
        if hideFirst:
            concatenatedData.append((i,) + data[i][1:])
        else:
            concatenatedData.append((i,) + data[i])

    # Color the headers
    if(headers != ""):
        headers     = list(headers)
        headers[0]  = "\033[1m" + headers[0]
        headers[-1] = headers[-1] + "\033[0m"
        headers     = tuple(headers)

    # Print table and prompt
    print(tabulate(concatenatedData, headers, tablefmt = TABLE_FMT))

    # Get user input, handle error if input is not an integer or the input is out of range
    if select:
        try:
        
            userChoice = int(input("\033[1m\033[32m$ \033[0m"))
            return data[userChoice]
            
        except (ValueError, IndexError): return None
    else: return False


"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ MAIN SCRIPT: Constants set-up and parsing command line arguments.                                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
ARGC        = len(sys.argv)
database    = DB.DB("diet.db", create = True)
journal     = database.access("journal")
nutrition   = database.access("nutrition")
TABLE_FMT   = "plain"

match sys.argv[1]:
    #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #┃ >> journal: Print all rows in the journal                                                                        ┃
    #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    case "journal":
        print(tabulate(journal.select(), journal.headers()))

    #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #┃ >> nutrition: Print all rows in the nutrition database                                                           ┃
    #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    case "nutrition":
        print(tabulate(nutrition.select(), nutrition.headers()))

    #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #┃ >> delete: Delete from nutrition database search term matching row and column parameters                         ┃
    #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    case "delete":
        try:
            # Get the search term
            deleteTerm = str(sys.argv[2])

            # If more arguments exist, parse those too
            if ARGC >= 4 and sys.argv[3] == "-c":
                searchColumn = str(sys.argv[4])
            else:
                searchColumn = None

            # Search objects. Skip if no results
            searchResults = nutrition.select(deleteTerm, searchColumn)
            if searchResults:
                choice = showTable(nutrition.select(deleteTerm, searchColumn), nutrition.headers())
                nutrition.delete(choice[0])
            else:
                print("No search results.")
                
        except IndexError: print("usage: delete <food name> (Optional: -c <search column>)")

    #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #┃ >> log: Add an entry to today from nutrition database. Prompts for serving size.                                 ┃
    #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    case "log":
        # Get user arguments
        searchTerm      = str(sys.argv[2]) if ARGC > 3 else None
        searchCol       = str(sys.argv[3]) if ARGC > 4 else None

        # Perform search
        searchResults   = nutrition.select(searchTerm, searchCol)

        # No selection prompt if search was empty
        if searchResults:
            choice = showTable(searchResults, nutrition.headers())
            if choice:
                food    = rowToFood(choice)
                today   = date.today().isoformat()
                journal.insert((None, today, food.name, food.cals, food.fats, food.carbs, food.protein, food.weight, food.volume, food.unit))
        else:
            print("No search results.")
            
    #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #┃ >> add: Add an entry to the  nutrition database.                                                                 ┃
    #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    case "add":
        # Get user arguments, catch errors
        try:
            # Put data into a tuple
            f = (str(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]),
                 float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8]), str(sys.argv[9]))

            # Add tuple to database
            try:
                nutrition.insert(f)
            except IntegrityError: # Replace entry if it already exists
                nutrition.delete(f[0])
                nutrition.insert(f)
                
        except (ValueError, IndexError):
            print("usage: add <food name> <cals> <fats> <carbs> <protein> <weight> <volume> <unit>")

        
    #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #┃ >> erase: Remove an entry logged. Search term may be provided, but is today by default.                          ┃
    #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    case "erase":
        # Get the search term. Fallback to today if the search date is not provided.
        searchTerm      = str(sys.argv[2]) if ARGC > 2 else date.today().isoformat()

        # Search objects
        searchResults   = journal.select(searchTerm, "date")
        
        # No selection prompt if search was empty
        if(searchResults):
            choice = showTable(searchResults, hideFirst = True)
            journal.delete(choice[0])
        else:
            print("No search results.")

    #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #┃ >> headers: view headers in nutrition.                                                                           ┃
    #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    case "headers":
        print(nutrition.headers())

    #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #┃ >> today: Show entries from today.                                                                               ┃
    #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    case "today":
        showTable(journal.select(str(date.today().isoformat()), "date"), journal.headers()[1:], hideFirst = True, select = False)
    
        

