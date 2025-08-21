# Food items are stored as dictionaries
# Ex. Banana: {
#   "name" : "Banana",
#   "cals" : 105.0,
#   "fats" : 0.4,
#   "carb" : 27.0,
#   "prot" : 1.3,
#   "mass" : {
#       "g" : 118.0,
#       "v"  : 1,
#       "u" : "Item"
#   }
# }

def cat(s1, s2, sep = " "):
    return s1 + sep + s2;

def init():
    # initializes fields for food item
    foodItem = {
        "name" : "",
        "cals" : 0,
        "fats" : 0,
        "carb" : 0,
        "prot" : 0,
        "mass" : {
            "g" : 0,
            "v" : 0,
            "u" : ""
        }
    }
    return foodItem

def combine(f1, f2):
    try:
        foodItem = {
            "name" : cat(f1["name"], f2["name"]),
            "cals" : f1["cals"] + f2["cals"],
            "fats" : f1["fats"] + f2["fats"],
            "carb" : f1["carb"] + f2["carb"],
            "prot" : f1["prot"] + f2["prot"],
            "mass" : {
                "g" : f1["mass"]["g"] + f2["mass"]["g"],
                "v" : f1["mass"]["v"] + f2["mass"]["v"],
                "u" : cat(f1["mass"]["u"], f2["mass"]["u"], sep = "\\")
            }
        }
        return foodItem
    except KeyError:
        return False
    except TypeError:
        return False


def make(payload):
    f = init()
    if(isinstance(payload, list)):
        f["name"] = payload[1]
        f["cals"] = payload[2]
        f["carb"] = payload[3]
        f["fats"] = payload[4]
        f["prot"] = payload[5]
        f["mass"]["g"] = payload[6]
        f["mass"]["v"] = payload[7]
        f["mass"]["u"] = payload[8]
        return f
    elif(isinstance(payload, str)):
        f["name"] = payload
        f["cals"] = input("Calories per serving: ")
        f["carb"] = input("Carbs per serving: ")
        f["fats"] = input("Fats per serving: ")
        f["prot"] = input("Protein per serving: ")
        f["mass"]["g"] = input("Grams per serving: ")
        f["mass"]["v"] = input("Volume per serving: ")
        f["mass"]["u"] = input("Volume Units: ")
        return f
    else:
        return False
