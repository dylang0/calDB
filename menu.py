import DB
import sys
import os

from sqlite3    import IntegrityError
from foodstruct import Food
from datetime   import date
from tabulate   import tabulate

"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚙ barChart3                                                               tuple(float) tuple(str) str int -> str ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Creates a coloured bar chart out of text strings based on given 3-element tuple. Raises ValueError if the data   ┃
┃ tuple sums to zero.                                                                                              ┃
┣━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Parameters  ┃ Type                     ┃ Description                                                             ┃
┣━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃   vec       │  tuple(float)            │ Data to build chart from.                                               ┃
┠─────────────┼──────────────────────────┼─────────────────────────────────────────────────────────────────────────┨
┃   colors    │  tuple(str)              │ Colors to use as ANSI escape codes.                                     ┃
┠─────────────┼──────────────────────────┼─────────────────────────────────────────────────────────────────────────┨
┃   chart     │  str                     │ The character to build the chart out of.                                ┃
┠─────────────┼──────────────────────────┼─────────────────────────────────────────────────────────────────────────┨
┃   size      │  int                     │ The maximum length of the string containing the chart.                  ┃
┗━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
def barChart3(vec, colors = ("\033[32m", "\033[34m", "\033[31m"), chart="━", size = 25):
    # Get total and check types
    total = float(vec[0]) + float(vec[1]) + float(vec[2])

    # Total is a divisor, so make sure it is not zero
    if total == 0: raise ValueError("Sum of elements should not be zero")

    # Create segments to join together as a string
    segments = tuple([ int(val/total * size) for val in vec ])

    # Display numbers if there is room. Otherwise, just make the chart.
    if size > 50:
        return "".join([color + chart * int(segment/2) + str(round(segment/size * 100, 1)) + "%" + chart * int(segment/2) for color, segment in zip(colors, segments)]) + "\033[0m"
    else:
        return "".join([color + chart * segment for color, segment in zip(colors, segments)]) + "\033[0m"

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
        data = journal.select()
        for i in range(len(data)):
            entry           = data[i]
            data[i]    = entry + (barChart3((entry[4], entry[5], entry[6])),)
        showTable(data, journal.headers() + ("",), hideFirst = False, select = False)

    #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #┃ >> nutrition: Print all rows in the nutrition database                                                           ┃
    #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    case "nutrition":
        data = nutrition.select()
        for i in range(len(data)):
            entry           = data[i]
            data[i]    = entry + (barChart3((entry[2], entry[3], entry[4])),)
        showTable(data, nutrition.headers() + ("",), hideFirst = False, select = False)

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
            # Add chart
            for i in range(len(searchResults)):
                entry            = searchResults[i]
                searchResults[i] = entry + (barChart3((entry[2], entry[3], entry[4])),)
            choice = showTable(searchResults, nutrition.headers() + ("",))
            if choice:
                serving = eval(input("Serving? \n\033[1m\033[32m$ \033[0m"))
                food    = rowToFood(choice)
                ratio   = float(serving)/food.weight
                food    = food * ratio
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
            choice = showTable(searchResults, headers = journal.headers(), hideFirst = True)
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
        # Get data
        todayData = journal.select(str(date.today().isoformat()), "date")

        # Combine macros
        kcal = 0
        fats = 0
        carb = 0
        prot = 0
        
        # Add chart
        for i in range(len(todayData)):
            entry           = todayData[i]
            kcal            = kcal + entry[3]
            fats            = fats + entry[4]
            carb            = carb + entry[5]
            protein         = prot + entry[6]
            print(entry)
            todayData[i]    = entry + (barChart3((entry[4], entry[5], entry[6])),)
        
        
        showTable(todayData, journal.headers()[1:] + ("",), hideFirst = True, select = False)
        print(f"\033[1mTotal Calories: {kcal} kcal\033[0m")
        print(barChart3((fats,carb,prot), size = 100))

    #┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    #┃ >> combine: Create 1 food entry from mulitple.                                                                   ┃
    #┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    case "combine":
        try:
            name       = str(sys.argv[2])
            food       = Food(name)
            searchTerm = input("\033[1m\033[32m$ \033[0mlog ")
            while(searchTerm):
                searchResults   = nutrition.select(searchTerm)
                if searchResults:
                    # Add chart
                    for i in range(len(searchResults)):
                        entry            = searchResults[i]
                        searchResults[i] = entry + (barChart3((entry[2], entry[3], entry[4])),)
                    choice = showTable(searchResults, nutrition.headers() + ("",))
                    if choice:
                        serving = input("Serving? \n\033[1m\033[32m$ \033[0m")
                        foodC   = rowToFood(choice)
                        ratio   = float(serving)/foodC.weight
                        foodC   = foodC * ratio
                        food    = food + foodC
                    else:
                        print("No search results.")
                searchTerm = input("\033[1m\033[32m$ \033[0mlog ")

            # Add combined item
            today   = date.today().isoformat()
            journal.insert((None, today, name, food.cals, food.fats, food.carbs, food.protein, food.weight, food.volume, food.unit))

                        
        except (ValueError, IndexError):
            print("usage: combine <food name>")
            
        

