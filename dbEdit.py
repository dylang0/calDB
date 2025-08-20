import sqlite3
import sys
from datetime import date

conn = sqlite3.connect("diet.db")
cursor = conn.cursor()

def add_entry(food, cals = 0.0, carb = 0.0, fats = 0.0, prot = 0.0):
    today = date.today().isoformat() # 2025-08-25
    cursor.execute("INSERT INTO entries (date, food, calories, carbohydrates, fats, protein) VALUES (?, ?, ?, ?, ?, ?)",
                    (today, food, cals, carb, fats, prot))
    print("Added " + food)
    conn.commit();

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
if not textIn:
    pass
elif textIn[0] == "view":
    view_entries()
elif textIn[0] == "log":
    cals = float(textIn[-4].strip())
    carb = float(textIn[-3].strip())
    fats = float(textIn[-2].strip())
    prot = float(textIn[-1].strip())
    name = "".join(textIn[1:-4])
    add_entry(name, cals, carb, fats, prot)
