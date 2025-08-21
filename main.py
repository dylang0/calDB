import dbEdit as db
import sys
from tabulate import tabulate

COMBINATION_ARG = "-c"
NEW_ARG = "-n"

print(None + None)

if len(sys.argv) > 1:
    match sys.argv[1]:
        case "log":
        
            try:
                if sys.argv[2] == NEW_ARG:
                    foodName = " ".join(sys.argv[3:])
                    print("\033[1m" + foodName)
                    db.logFromNew(foodName)
                else:
                    foodName = " ".join(sys.argv[2:])
                    db.search(foodName)
            except IndexError:
                print("Usage: log <fooditem>")
        case "add":
            pass
        case "history":
            pass
        case "today":
            db.showToday()
        case "find":
            entries = db.search(sys.argv[2])
            print(tabulate(entries, headers=["ID", "Name", "Cals", "Carbs", "Fats", "Protein"]))
        case _:
            print("\033[1m[?] Unrecognized Argument " + sys.argv[1])
