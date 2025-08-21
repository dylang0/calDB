import sqlite3
import sys
from datetime import date
from tabulate import tabulate

conn = sqlite3.connect("diet.db")
cursor = conn.cursor()

def parseEntry(wordList):
    # -------------------------------------------------
    NUM_ARGS        = 8
    DICT_KEYS       = ["name", "cals", "weight_g", "carb", "fats", "prot", "vol_unit", "volume"]
    DICT_VALS       = ["",      None,   None,       None,   None,   None,   "Unit",     1]
    l               = len(wordList)
    wordDict        = {}
    # -------------------------------------------------
    for i in range(l):
        DICT_VALS[i] = wordList[i]
    return dict(zip(DICT_KEYS, DICT_VALS))
    # -------------------------------------------------

def showToday():
    today = date.today().isoformat() # 2025-08-20
    cursor.execute("SELECT * FROM entries WHERE date = ?", (today,))
    entries = cursor.fetchall()
    table = []
    relativeIndex = 0
    for entry in entries:
        table.append( (relativeIndex,) + entry[2:])
        relativeIndex += 1
    print(tabulate(table, headers=["ID", "Name", "Cals", "Carbs", "Fats", "Protein"]))

def addEntry(foodName, cals, weight_g, carbs, fats, prot, vol_unit, volume):
    cursor.execute("INSERT INTO foodList(food, calories, weight_g, carbohydrates, fats, protein, vol_unit, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (foodName, cals, weight_g, carbs, fats, prot, vol_unit, volume))
    conn.commit()
    print("Added " + BOLD + foodName)
    
def search(foodName):
    cursor.execute("SELECT * FROM foodList WHERE food LIKE ?", ("%" + foodName + "%",))
    entries = enumerate(cursor.fetchall())
    return(entries)

def select(foodName):
    entries = search(foodName)
    table = []
    relativeIndex = 0
    for entry in entries:
        table.append( (relativeIndex,) + entry[2:])
        relativeIndex += 1
    #print(tabulate(table, headers=["ID", "Name", "Cals", "Carbs", "Fats", "Protein"]
    

def logFromEntry(foodName):
    results = search(foodName)
    l = len(list(results))
    if(l == 0):
        return None
    elif(l == 1):
        pass
        # log only result by weight
    else:
        try:
            response = str(input("Select which item to use by ID: "))
            
        except ValueError:
            print("Error: Input must be a number")
        # select a result
        
    
def logFromNew(name):
    cals = input("Calories (g): ")
    carb = input("Carbohydrates (g): ")
    fats = input("Fats (g): ")
    prot = input("Protein (g): ")
    today = date.today().isoformat() # 2025-08-20
    cursor.execute("INSERT INTO entries (date, food, calories, carbohydrates, fats, protein) VALUES (?, ?, ?, ?, ?, ?)",
                    (today, name, cals, carb, fats, prot))
    conn.commit();
    showToday()

#def add_entry(food, cals = 0.0, carb = 0.0, fats = 0.0, prot = 0.0):
#    today = date.today().isoformat() # 2025-08-25
#    cursor.execute("INSERT INTO entries (date, food, calories, carbohydrates, fats, protein) VALUES (?, ?, ?, ?, ?, ?)",
#                    (today, food, cals, carb, fats, prot))
#    print("Added " + food)
#    conn.commit();

def view_entries():
    cursor.execute("SELECT * from entries;")
    entries = cursor.fetchall()
    for entry in entries:
        print(entry)
