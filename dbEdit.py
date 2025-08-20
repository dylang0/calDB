import sqlite3
import sys
from datetime import date

# ANSI Escape Codes
BOLD    = "\033[1m"
REG     = "\033[0m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[37m"
WHITE   = "\033[37m"

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

def addEntry(foodName, cals, weight_g, carbs, fats, prot, vol_unit, volume):
    cursor.execute("INSERT INTO foodList(food, calories, weight_g, carbohydrates, fats, protein, vol_unit, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (foodName, cals, weight_g, carbs, fats, prot, vol_unit, volume))
    conn.commit()
    print("Added " + BOLD + foodName)
    
    

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

# Input Handling
#if len(sys.argv) == 1:
print("Usage:\tlog <food> To log and item from the food list")
print("\tlog <food> <cals> <carbs> <fat> <prot> To log a custom entry")
print("\tadd <food> <cals> <carbs> <fat> <prot> To add an item to the food list")
print("\tview To view entries")
textIn = input("calDB> ").split()
textIn = parseEntry(textIn)

addEntry(textIn["name"], textIn["cals"], textIn["weight_g"], textIn["carb"], textIn["fats"], textIn["prot"], textIn["vol_unit"], textIn["volume"])
#if not textIn:
#    pass
#elif textIn[0] == "view":
#    view_entries()
#elif textIn[0] == "log":
#    cals = float(textIn[-4].strip())
#    carb = float(textIn[-3].strip())
#    fats = float(textIn[-2].strip())
#    prot = float(textIn[-1].strip())
#    name = "".join(textIn[1:-4])
#    add_entry(name, cals, carb, fats, prot)
