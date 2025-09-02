import sys
from datetime   import date
from DB         import DB
from tabulate   import tabulate

# -----------------------------------------
# Constants
ARGC            = len(sys.argv)
TABLE_FORMAT    = "plain"
# -----------------------------------------

# ------------------------------------------------------------------------------------------- #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ------------------------------------------------------------------------------------------- #
# Makes nice looking charts
def split3(x, y, z, colors = ("\033[34m", "\033[32m", "\033[31m"), chart="━", size = 25):
    if any([not isinstance(val, (int, float)) for val in (x, y, z)]):
        raise ValueError
    total = x + y + z
    if total == 0: return ""
    segments = tuple([int(val/total * size) for val in (x, y, z)])
    if size > 50:
        return "".join([color + chart * int(segment/2) + str(round(segment/size * 100, 1)) + "%" + chart * int(segment/2) for color, segment in zip(colors, segments)]) + "\033[0m"
    else:
        return "".join([color + chart * segment for color, segment in zip(colors, segments)]) + "\033[0m"
# ------------------------------------------------------------------------------------------- #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ------------------------------------------------------------------------------------------- #
# Displays tabulated data to the user and prompts them to pick a row.
def chooseFromTable(data, headers, chartDataCols = (2, 3, 4)):
    nrow = len(data)

    # Append column for row indices and a column for the chart
    tableData = []
    for i in range(nrow):
        tableData.append( ( f"\033[1m{i}\033[0m" ,) + data[i] )
    
    # Add space to headers to reflect the new column
    print("\033[1m", tabulate(tableData, tablefmt = TABLE_FORMAT, headers = headers))

    # Get selection of choice and serving
    choice = input("\033[1m\033[34m> \033[0m").split()

    # Try to convert first to int
    choice = [float(x) for x in choice]
    choice[0] = int(choice[0])

    # If choice was out of range, this is an error
    if choice[0] < 0 or choice[0] >= nrow: raise IndexError

    # return entries
    return (choice)
    
# ------------------------------------------------------------------------------------------- #
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
# ------------------------------------------------------------------------------------------- #

# Main Loop
if ARGC == 1:
    print(f"\033[34musage: {sys.argv[0]} [<option>]\033[0m",
           "\nOperations:",
           "\tlog\t\tAdd an entry for today from saved food",
           "\terase\t\tDelete an entry from today",
           "\ttoday\t\tShow today's entries",
           "\tadd\t\tAdd item to the nutrition database",
           "\tdelete\t\tDelete item from the nutrition database",
           "\tsaved\t\tShow saved items in nutrition database",
           sep="\n")
else:
    # Load database since we are trying to access it now
    database    = DB("diet.db")
    journal     = DB.TB(database, "entries")
    nutrition   = DB.TB(database, "list")

    # Direct path based on first argument
    match sys.argv[1]:
    # ┌───────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ > LOG: Add an entry to the journal.                                                           │
    # └───────────────────────────────────────────────────────────────────────────────────────────────┘
        case "log":
            # Get next arguments, but catch indexing error and display usage help message.
            # Automatically searches by the name in the nutrition table
            try:
                searchTerm      = sys.argv[2]

                # Perform search
                results         = nutrition.select(searchTerm)

                # Append macro chart to data
                # When searching from the nutrition table, the macros are in positions 2, 3, and 4
                for i in range(len(results)):
                    entry       = results[i]
                    results[i]  = entry + ( split3(entry[2], entry[3], entry[4]), )

                
                # Get selection from user, add space to headers to reflect new chart column
                response        = chooseFromTable(results, nutrition.headers() + ("",) )
                response        = (response[0], response[1])

                # Convert to new entry based on responses
                selection       = results[response[0]]
                servingRatio    = response[1]/selection[5]
                newEntry        = (None, str(date.today().isoformat()), selection[0],
                                   selection[1] * servingRatio,
                                   selection[2] * servingRatio,
                                   selection[3] * servingRatio,
                                   selection[4] * servingRatio,
                                   selection[5] * servingRatio,
                                   selection[6])

                # Add to journal
                journal.insert(newEntry)

            # Error handling
            except (IndexError, ValueError):
                print(f"\033[34musage: {sys.argv[0]} log <food name>\033[0m")
                
    # ┌───────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ > ERASE: Delete an entry from today.                                                          │
    # └───────────────────────────────────────────────────────────────────────────────────────────────┘
        case "erase":
            try:
                # Perform search on todays entries
                results         = journal.select(str(date.today().isoformat()), "date")
                
                # Hide the IDs from the journal, create "display result" set
                toDisplay       = []
                for i in range(len(results)):
                    entry       = results[i][1:]
                    toDisplay.append( (i,) + entry + (split3(entry[3], entry[4], entry[5]), ) )

                # Get selection from user, add space to headers to reflect new chart column
                response       = chooseFromTable(toDisplay, journal.headers() + ("",))[0]

                # Get ID to delete
                toDelete       = results[response][0]

                # Erase
                journal.delete(toDelete)

            # Error handling
            except IndexError:
                pass
    # ┌───────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ > DELETE: Delete an entry in the nutrition data.                                              │
    # └───────────────────────────────────────────────────────────────────────────────────────────────┘
        case "delete":
            try:
                searchTerm      = sys.argv[2]

                # Perform search
                results         = nutrition.select(searchTerm)

                # Append macro chart to data
                # When searching from the nutrition table, the macros are in positions 2, 3, and 4
                for i in range(len(results)):
                    entry       = results[i]
                    results[i]  = entry + ( split3(entry[2], entry[3], entry[4]), )

                
                # Get selection from user, add space to headers to reflect new chart column
                response        = chooseFromTable(results, nutrition.headers() + ("",) )[0]
                toDelete        = results[response][0]
                
                # Convert to new entry based on responses
                nutrition.delete(toDelete)

                

            # Error handling
            except (IndexError, ValueError):
                print(f"\033[34musage: {sys.argv[0]} log <food name>\033[0m")
    # ┌───────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ > ADD: Add entry to nutrition data.Add                                                        │
    # └───────────────────────────────────────────────────────────────────────────────────────────────┘
        case "add":
            newEntry = tuple(sys.argv[2:])
            nutrition.insert(newEntry)
    # ┌───────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ > TODAY: Display todays entries.                                                              │
    # └───────────────────────────────────────────────────────────────────────────────────────────────┘
        case "today":
            # Perform search on todays entries
            results         = journal.select(str(date.today().isoformat()), "date")
                            
            # Hide the IDs from the journal, create "display result" set
            toDisplay       = []
            for i in range(len(results)):
                entry       = results[i][1:]
                toDisplay.append( (entry + (split3(entry[3], entry[4], entry[5]), ) ))

            nrow = len(toDisplay)
            
            # Append column for row indices and a column for the chart
            tableData = []
            
            for i in range(nrow):
                tableData.append( ( f"\033[1m{i}\033[0m" ,) + toDisplay[i] )
                
            # Add space to headers to reflect the new column
            print("\033[1m", tabulate(tableData, tablefmt = TABLE_FORMAT, headers = journal.headers() + ("",)))
            
