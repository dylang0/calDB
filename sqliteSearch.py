import sqlite3
import sys
import curses
import foodItems
from tabulate import tabulate
from datetime import date

conn = sqlite3.connect("diet.db")
cursor = conn.cursor()

DEFAULT_DB = "foodList"
DEFAULT_SELECT_MSG = "Select an Entry: "
VALID_TABLES = ("entries", "foodList")

def search(target, db = DEFAULT_DB, showResults = True):
    # --------------------------------------------------------------------------------
    if db not in VALID_TABLES:
        raise ValueError("Invalid table name")
    
    # note that "food" is the identifier for names in both databases
    if db == "foodList":
        cursor.execute(f"SELECT * FROM {db} WHERE food LIKE ?", ("%" + target + "%",))
    else: # db == "entries"
        cursor.execute(f"SELECT * FROM {db} WHERE date = ?", (target,))
    results = enumerate(cursor.fetchall())
    entryList = []
    # --------------------------------------------------------------------------------
    for entry in results:
        entry = list((entry[0],) + entry[1])
        entryList.append(entry)
    # --------------------------------------------------------------------------------
    if len(entryList) == 0:
        showResults = False
        print("No search results")
    # --------------------------------------------------------------------------------
    if showResults:
        if db == "foodList":
            dbHeaders = ["ID"] + [description[0] for description in cursor.description]
            print(tabulate(entryList, headers = dbHeaders))
        else: # db == "entries"
            dbHeaders = [description[0] for description in cursor.description]
            prettyList = []
            for entry in entryList:
                prettyList.append([entry[0]] + entry[2:])
            print(tabulate(prettyList, headers = dbHeaders))
    # --------------------------------------------------------------------------------
    return entryList

def select(target, db = DEFAULT_DB, message = DEFAULT_SELECT_MSG):
    # --------------------------------------------------------------------------------
    entries = search(target, db, showResults = True)
    # --------------------------------------------------------------------------------
    if len(entries) == 0:
        return False
    # --------------------------------------------------------------------------------
    try:
        response = int(input(message))
        selection = entries[response]
        return selection
    # --------------------------------------------------------------------------------
    except ValueError:
        print("Cancelling")
        return False
    except IndexError:
        print("Index out of range")
        return False
    # --------------------------------------------------------------------------------

def remove(target, db):
    item = select(target, db)
    if(item):
        name = item[1] if db == "foodList" else item[3]
        response = input(f"Are you sure you want to remove {name}? (y/n) " )
        if(response == "y"):
            if(db == "foodList"):
                cursor.execute(f"DELETE FROM {db} WHERE food = ?", (name,))
                conn.commit()
            elif(db == "entries"):
                cursor.execute(f"DELETE FROM {db} WHERE id = ?", (item[1],))
                conn.commit()
                

def add(food, db):
    if db not in VALID_TABLES:
        raise ValueError("Invalid table name")

    if db == "foodList":
        headersStr = "(food, calories, carbohydrates, fats, protein, weight_g, volume, vol_unit)"
        cursor.execute(f"INSERT INTO {db} {headersStr} VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (food["name"], food["cals"], food["carb"], food["fats"],
                         food["prot"], food["mass"]["g"], food["mass"]["v"], food["mass"]["u"]))
    else: # db == "entries"
        headersStr = "(date, food, calories, carbohydrates, fats, protein, weight_g, volume, vol_unit)"
        today = date.today().isoformat() # 2025-08-21
        cursor.execute(f"INSERT INTO {db} {headersStr} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (today, food["name"], food["cals"], food["carb"], food["fats"],
                               food["prot"], food["mass"]["g"], food["mass"]["v"], food["mass"]["u"]))
    conn.commit()   

def showAll(db = "entries"):
    if db not in VALID_TABLES:
            raise ValueError("Invalid table name")

    cursor.execute(f"SELECT * FROM {db}")
    results = cursor.fetchall()
    entryList = []
    for entry in results:
            entryList.append(entry[1:]) if db == "entries" else entryList.append(entry)
    if db == "foodList":
        dbHeaders = ["Food", "Cals", "Carbs", "Fats", "Protein", "Weight (g)", "Volume", "Units"]
    else: # db == "entries"
        dbHeaders = ["Date", "Food", "Cals", "Carbs", "Fats", "Protein", "Weight (g)", "Volume", "Units"]
    print(tabulate(entryList, headers = dbHeaders))
