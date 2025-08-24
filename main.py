#!/usr/bin/env python3
import TableIO as Tb
import sys
from datetime import date
from tabulate import tabulate

running = True
fields = ["food", "calories", "carbohydrates", "fats", "protein", "mass", "m_unit"]

def select(db, term, col="food", headers=fields, message="$ ", clipFirst=False):
    results = db.search(term, col)
    if(clipFirst):
        cleaned = []
        for entry in results:
            cleaned.append(entry[1:])
        print(tabulate(cleaned, showindex="always", headers=headers))
    else:
        print(tabulate(results, showindex="always", headers=headers))
    index = int(input(message))
    try:
        selection = results[index]
    except IndexError:
        selection = False
    return selection

def log(cm):
    l = len(cmd)
    today = date.today().isoformat()
    if(cmd[1] == "-n"):
        name = " ".join(cmd[2:l - 6])
        database.setTable("entries")
        database.write(data=[today, name]+cmd[-6:], headers=["date"]+fields)
    else:
        name = " ".join(cmd[1:])
        database.setTable("list")
        s = list(select(database, name))
        mult = float(input("Serving? "))/s[-2]
        for i in range(1, 6):
            s[i] = s[i] * mult
        database.setTable("entries")
        database.write(data=[today]+s, headers=["date"]+fields)

database = Tb.TableIO("diet.db", "list")

while running:
    cmd = input("log\t\t-l [ -n ] <name> [<cals> <carb> <fats> <prot> <mass> <unit>] \n"
                + "combine\t\t-c <integer number of items>\n"
                + "unregister\t-u <date>\n"
                + "write\t\t-w <name> <cals> <carb> <fats> <prot> <mass> <unit>\n"
                + "erase\t\t-e <name>\n"
                + "today\t\t-t\n"
                + "database\t-d\n"
                + "journal\t\t-j\n"
                + "quit\t\t-q\n"
                + "$ ").split(" ")
    match cmd[0]:
        case "-l":
            l = len(cmd)
            today = date.today().isoformat()
            if(cmd[1] == "-n"):
                name = " ".join(cmd[2:l - 6])
                database.setTable("entries")
                database.write(data=[today, name]+cmd[-6:], headers=["date"]+fields)
            else:
                name = " ".join(cmd[1:])
                database.setTable("list")
                s = list(select(database, name))
                mult = float(input("Serving? "))/s[-2]
                for i in range(1, 6):
                    s[i] = s[i] * mult
                database.setTable("entries")
                database.write(data=[today]+s, headers=["date"]+fields)
        case "-c":
            if int(cmd[1]) < 2: pass
            newFood = ["", 0, 0, 0, 0, 0, "g"]
            for i in range(int(cmd[1])):
                print(f"==> {i} <==")
                subCMD = input("log\t\t-l [ <name> | -n <cals> <carb> <fats> <prot> <mass> <unit>] \n"
                                + "cancel\t\t-c\n"
                                + "$ ").split(" ")
                if subCMD[0] == "-l":
                    if subCMD[1] == "-n":
                        for i in range(1,6): newFood[i] += float(subCMD[i+1])
                    else:
                        name = " ".join(subCMD[1:])
                        database.setTable("list")
                        s = list(select(database, name))
                        mult = float(input("Serving? "))/s[-2]
                        for i in range(1, 6):
                            s[i] = float(s[i]) * mult
                        for i in range(1, 6): newFood[i] += float(s[i])
                elif subCMD[0] == "-c":
                    break
                else:
                    i = i -1
            today = date.today().isoformat()
            newFood[0] = input("Name? ")
            database.setTable("entries")
            database.write(data=[today]+newFood, headers=["date"]+fields)
                                
            
            
        case "-u":
            database.setTable("entries")
            day = date.today().isoformat() if len(cmd) == 1 else " ".join(cmd[1:])
            s = select(database, day, col="date", headers=["date"]+fields, clipFirst=True)
            database.erase(s[0], "id")
        case "-w":
            l = len(cmd)
            name = " ".join(cmd[1:l - 6])
            database.setTable("list")
            database.write(data=[name]+cmd[-6:])
        case "-e":
            name = " ".join(cmd[1:])
            database.setTable("list")
            s = select(database, name)
            database.erase(s[0], "food")
        case "-t":
            today = date.today().isoformat()
            database.setTable("entries")
            raw = database.search(today, "date")
            cleaned = []
            for entry in raw:
                cleaned.append(entry[1:])
            print("\n", tabulate(cleaned, headers=["date"]+fields), "\n")
        case "-d":
            database.setTable("list")
            s=database.all()
            if(len(s) == 0):
                print("\nNo data.\n")
            else:
                print("\n", tabulate(s, headers=fields), "\n")
            
        case "-j":
            database.setTable("entries")
            s=database.all()
            if(len(s) == 0):
                print("\nNo entries.\n")
            else:
                print("\n", tabulate(s, headers=["ID", "date"]+fields), "\n")
        case "-q":
            running = False
    
