import TableIO as Tb
import sys
from tabulate import tabulate

running = True
stage = 1

while running:
    match stage:
        case 1:
            if(len(sys.argv) > 2):
                cmd = ["-i", sys.argv[1], sys.argv[2]]
            else:
                cmd = input("Init \t -i <database.db> <table>\nQuit \t -q\n$ ").split()
            match cmd[0]:
                case "-i":
                    try:
                        file = cmd[1]
                        table = cmd[2]
                        database = Tb.TableIO(file, table)
                        stage = 2
                    except IndexError:
                        pass
                    except ValueError as error:
                        print(error)
                        running = False
                        pass
                case "-q":
                    running = False
                    pass
        case 2:
            if(len(sys.argv) > 5):
                cmd = [sys.argv[3], sys.argv[4], sys.argv[5]]
            else:
                cmd = input("Search\t-s <term> <column>\nWrite\t-w <d0> <d1> <d2> ...\nErase\t-e <term> <column>\nQuit\t-q\n$ ").split()
            match cmd[0]:
                case "-s":
                    try:
                        print(tabulate(database.search(cmd[1], cmd[2])))
                    except IndexError: 
                        pass
                    except Tb.sqlite3.OperationalError as error:
                        print(error)
                        running = False
                case "-w":
                    try:
                        args = []
                        for i in range(1, len(cmd)):
                            args.append(cmd[i])
                        print(args)
                        database.write(args)
                    except IndexError:
                        pass
                    except Tb.sqlite3.OperationalError as error:
                        print(error)
                case "-e":
                    try:
                        database.erase(cmd[1], cmd[2])
                    except IndexError:
                        pass
                    except Tb.sqlite3.OperationalError as error:
                        print(error)
                case "-q":
                    running = False
                    pass
