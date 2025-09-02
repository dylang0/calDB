# ┌─────────────────────────────────────────────────────────────────────────────────────┐
# │  The food class is essentially a dictionary with fixed keys.                        │
# │  It carries nutrition information.                                                  │
# │  It can be used to easily transfer data between food databases.                     │
# │                                                                                     │
# │     ┏━━━━━━━━━━━━━━━━━┓                                                             │
# │     ┃ 🥚 EGG          ┃                                                             │
# │     ┣━━━━━━━━━━━┳━━━━━┫                                                             │
# │     ┃ cals      ┃ ... ┃                                                             │
# │     ┃ fats      ┃ ... ┃                                                             │
# │     ┃ carbs     ┃ ... ┃                                                             │
# │     ┃ protein   ┃ ... ┃                                                             │
# │     ┃ mass      ┃ ... ┃                                                             │
# │     ┗━━━━━━━━━━━┻━━━━━┛                                                             │
# │                                                                                     │
# │  Functions Defined                                                                  │
# │     • __init__                                                                      │
# │     • __add__                                                                       │
# │     • __mul__                                                                       │
# │     • __sub__                                                                       │
# │     • __truediv__                                                                   │
# │     • __repr__                                                                      │
# └─────────────────────────────────────────────────────────────────────────────────────┘
class Food:
    # ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ Initializes member variables and enforces data types. Raises ValueError if there as an issue with input types.   │
    # └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    def __init__(self, name  = "", cals = 0, fats = 0, carbs = 0, protein = 0, weight = 0, volume = 0, unit = "?"):
        self.name       = str(name)
        self.cals       = float(cals)
        self.fats       = float(fats)
        self.carbs      = float(carbs)
        self.protein    = float(protein)
        self.weight     = float(weight)
        self.volume     = float(volume)
        self.unit       = str(unit)

    # ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ Overloads the "+" operator.                                                                                      │
    # └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    def __add__(self, other):
        # Force 'other' to be another food object
        if not type(other) is Food: raise ValueError
        
        # Initialize new food object to return later.              
        f = Food()

        # Add attributes
        f.name      = self.name + ", "  + other.name
        f.cals      = self.cals         + other.cals
        f.fats      = self.fats         + other.fats
        f.carbs     = self.carbs        + other.carbs
        f.protein   = self.protein      + other.protein
        f.weight    = self.weight       + other.weight

        # If the units are the same, add them together.
        # Otherwise, the units will be undefined.
        if self.unit == other.unit:
            f.volume    = self.volume + other.volume
            f.unit      = self.unit
        else:
            f.volume    = "?"
            f.units     = 0
            
        # Return the completed sum
        return f        
    
    # ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ Overloads the "*" operator.                                                                                      │
    # └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    def __mul__(self, val):
        # Force 'val' to be a floating point number
        val = float(val)

        # Initialize new food object to return later.              
        f = Food()
        
        # Multiply attributes
        f.name      = self.name
        f.cals      = self.cals     * val
        f.fats      = self.fats     * val
        f.carbs     = self.carbs    * val
        f.protein   = self.protein  * val
        f.weight    = self.weight   * val
        f.volume    = self.volume   * val
        f.unit      = self.unit

        # Return the completed product
        return f

    # ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ Overloads the "-" operator.                                                                                      │
    # └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    def __sub__(self, other):
        return self + (other * -1)

    # ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ Overloads the "/" operator.                                                                                      │
    # └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    def __truediv__(self, other):
        # Force 'val' to be a floating point number
        val = float(val)

        # Initialize new food object to return later.              
        f = Food()
        
        # Multiply attributes
        f.name      = self.name
        f.cals      = self.cals     / val
        f.fats      = self.fats     / val
        f.carbs     = self.carbs    / val
        f.protein   = self.protein  / val
        f.weight    = self.weight   / val
        f.volume    = self.volume   / val
        f.unit      = self.unit

        # Return the completed product
        return f
        
    # ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ String representation for print()                                                                                │
    # └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    def __repr__(self):
        # Generate a dictionary and return the string representation
        return str({attr : getattr(self, attr) for attr in self.__dict__})

    # ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
    # │ Object iterable.                                                                                                 │
    # └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
    def __iter__(self):
        for attr in self.__dict__:
            yield getattr(self, attr)
