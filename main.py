import dbReaderWriter as db
import sys

from tabulate import tabulate
from datetime import date

argc = len(sys.argv)
TABLE_FORMAT = "plain"

def split3(x, y, z, colors = ("\033[34m", "\033[32m", "\033[31m"), chart="━", size = 25):
    if any([not isinstance(val, (int, float)) for val in (x, y, z)]):
        raise ValueError
    total = x + y + z
    segments = tuple([int(val/total * size) for val in (x, y, z)])
    if size > 50:
        return "".join([color + chart * int(segment/2) + str(round(segment/size, 1)*100) + "%" + chart * int(segment/2) for color, segment in zip(colors, segments)]) + "\033[0m"
    else:
        return "".join([color + chart * segment for color, segment in zip(colors, segments)]) + "\033[0m"
    
    

if(argc == 1):
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
    Database = db.dbReaderWriter("diet.db", create=True)
    Journal = Database.access("entries")
    Nutrition = Database.access("list")
    match sys.argv[1]:
        case "log":
            try:
                searchTerm = sys.argv[2]

                results = Nutrition.read(searchTerm)
                l = len(results["food"])
                tableData = { "\033[1mID" : tuple([ "\033[1m" + str(x) + "\033[0m" for x in range(l) ]) }
                tableData.update(results)
                chartData = ()
                for i in range(l):
                    chartData = chartData + (split3(results["carbohydrates"][i], results["fats"][i], results["protein"][i]),)
                tableData["chart"] = chartData
                print(tabulate(tableData, headers="keys", tablefmt=TABLE_FORMAT))
                
                selection = input("\033[1m\033[32m$ \033[0m").split()
                
                if(len(selection) < 2):
                    print(f"\033[34musage: <index ID> <serving size>\033[0m")
                else:
                    index = int(selection[0])
                    foodObj = {}
                    for key, value in results.items():
                        foodObj[key] = value[index]

                    
                    servingRatio = float(selection[1])/foodObj["mass"]
                    for i in ("calories", "carbohydrates", "fats", "protein", "mass"):
                        foodObj[i] = round(foodObj[i] * servingRatio, 1)

                    foodObj["date"] = str(date.today().isoformat())
                    foodObj["id"] = None
                    
                    Journal.write(foodObj)
                
            except IndexError:
                print(f"\033[34musage: {sys.argv[0]} log <food name>\033[0m")
        case "today":
            results = Journal.read(date.today().isoformat(), "date")
            results.pop("id")
            
            l = len(results["food"])
            
            tableData = { "\033[1mID" : tuple([ "\033[1m" + str(x) + "\033[0m" for x in range(l) ]) }
            tableData.update(results)
            
            print(tabulate(tableData, headers="keys", tablefmt=TABLE_FORMAT))

            totals = []
            for nutrient in ("calories", "carbohydrates", "fats", "protein"):
                totals.append(sum(x for x in results[nutrient]))
            print("Calories Today: ", totals[0], " kcal")
            print(split3(totals[1], totals[2], totals[3], size=100))
        case "erase":
            try:
                results = Journal.read(date.today().isoformat(), "date")
                hiddenIDs = results.pop("id")
                l = len(results["food"])
                tableData = { "\033[1mID" : tuple([ "\033[1m" + str(x) + "\033[0m" for x in range(l) ]) }
                tableData.update(results)
                chartData = ()
                for i in range(l):
                    chartData = chartData + (split3(results["carbohydrates"][i], results["fats"][i], results["protein"][i]),)
                tableData["chart"] = chartData
                print(tabulate(tableData, headers="keys", tablefmt=TABLE_FORMAT))
                
                selection = input("\033[1m\033[32m$ \033[0m").split()
                
                if(len(selection) < 1):
                    print(f"\033[34musage: <index ID>\033[0m")
                else:
                    index = int(selection[0])
                    toDelete = hiddenIDs[index]
                    Journal.erase(toDelete)
                
            except IndexError:
                print(f"\033[34musage: {sys.argv[0]} erase <food name>\033[0m")
        case "add":
            if(argc < 9):
                print(f"\033[34musage: {sys.argv[0]} add <food name> <cals> <carbs> <fats> <protein> <mass> <unit>\033[0m")
            else:
                data = sys.argv[-6:]
                name = " ".join(sys.argv[2:-6])
                data = [name] + data
                data[0] = data[0]
                data[6] = data[6]
                #print(data)
                Nutrition.write(data)
        case "saved":
            results = Nutrition.read()
            l = len(results["food"])
            tableData = { "\033[1mID" : tuple([ "\033[1m" + str(x) + "\033[0m" for x in range(l) ]) }
            tableData.update(results)
            chartData = ()
            for i in range(l):
                chartData = chartData + (split3(results["carbohydrates"][i], results["fats"][i], results["protein"][i]),)
                tableData["chart"] = chartData
            print(tabulate(tableData, headers="keys", tablefmt=TABLE_FORMAT))
        case "delete":
            try:
                searchTerm = sys.argv[2]

                results = Nutrition.read(searchTerm)
                l = len(results["food"])
                tableData = { "\033[1mID" : tuple([ "\033[1m" + str(x) + "\033[0m" for x in range(l) ]) }
                tableData.update(results)
                chartData = ()
                for i in range(l):
                    chartData = chartData + (split3(results["carbohydrates"][i], results["fats"][i], results["protein"][i]),)
                tableData["chart"] = chartData
                print(tabulate(tableData, headers="keys", tablefmt=TABLE_FORMAT))
                
                selection = input("\033[1m\033[32m$ \033[0m").split()
                
                if(len(selection) < 1):
                    print(f"\033[34musage: <index ID>\033[0m")
                else:
                    index = int(selection[0])
                    toDelete = results["food"][index]
                    Nutrition.erase(toDelete)
                
            except IndexError:
                print(f"\033[34musage: {sys.argv[0]} delete <food name>\033[0m")
        case "test":
            split3(10, 30, 60)
        
