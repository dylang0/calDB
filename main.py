import dbEdit as db
import sys
import foodItems
import sqliteSearch as sqs
from datetime import date
from tabulate import tabulate

COMBINATION_ARG = "-c"
NEW_ARG = "-n"

def getRatio(choice):
    multiplier = input("How much? <value> [g|Tbsp|tsp|Cup]: ")
    args = multiplier.split()
    if(len(args) == 1):
        multiplier = 1
    elif(args[2] == "g"):
        multiplier = float(args[1])/float(choice[6])
    else:
        multiplier = float(args[1])/float(choice[7])
    for i in range(2, 7):
        choice[i] = choice[i] * multiplier
    return choice


if len(sys.argv) > 1:
    match sys.argv[1]:
        case "log":
        
            try:
                if sys.argv[2] == NEW_ARG:
                    foodName = " ".join(sys.argv[3:])
                    item = foodItems.make(foodName)
                    sqs.add(item, "entries")
                elif sys.argv[2] == COMBINATION_ARG:
                    foodName = " ".join(sys.argv[3:])
                    item = foodItems.init()
                    for i in range(sys.argv[3]):
                        response = input("Select from list? (y/n) ")
                        if(response == "y"):
                            foodName = input("Search for: ")
                            choice = sqs.select(foodName)
                            if(choice):
                                choice = getRatio(choice)
                                selection = foodItems.make(choice)
                                item = foodItems.combine(item, selection)
                            else:
                                i = i - 1
                        else:
                            foodName = input("Name of Item: ")
                            selection = foodItems.make(foodName)
                            item = foodItems.combine(item, selection)
                    item["name"] = foodName
                    sqs.add(item, "entries")
                else:
                    foodName = " ".join(sys.argv[2:])
                    choice = sqs.select(foodName)
                    if(choice):
                        choice = getRatio(choice)
                        item = foodItems.make(choice)
                        sqs.add(item, "entries")
            except IndexError:
                print("Usage: log <fooditem>"),
        case "delete":
            sqs.remove(date.today().isoformat(), "entries")
        case "add":
            foodName = " ".join(sys.argv[2:])
            item = foodItems.make(foodName)
            sqs.add(item, "foodList")
        case "remove":
            foodName = " ".join(sys.argv[2:])
            sqs.remove(foodName, "foodList")
        case "history":
            sqs.showAll()
            pass
        case "today":
            sqs.search(date.today().isoformat(), "entries")
        case "find":
            sqs.search(sys.argv[2], "foodList")
        case "saved":
            sqs.showAll("foodList")
        case _:
            print("\033[1m[?] Unrecognized Argument " + sys.argv[1])
