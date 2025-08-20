import sqlite3
from datetime import date

conn = sqlite3.connect("diet.db")
curs = conn.cursor()

def add_entry(food, cals, carb = 0, fats = 0, prot = 0):
    today = date.today().isoformat() # 2025-08-25
    cursor.execute("INSERT INTO entries (date, food, calories, carbohydrates, fats, protein) VALUES (?, ?, ?, ?, ?, ?)",
                    (today, food, cals, carb, fats, prot))
    conn.commit();
