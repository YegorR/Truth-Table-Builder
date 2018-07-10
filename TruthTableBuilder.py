# На вход подаётся формула, которая включает в себя:
# латинские буквы, символы 1 и 0, + или |, * или &, -, (), =, >
# используется регуларное выражение [^01\+|\*&()\-a-zA-Z\s=>]
import re
from Node import *

try:
    formula = input("Enter the logic formula:\n")
    formula = formula.strip()
    while re.search("[^01\+|\*&()\-a-zA-Z\s=>]",formula) != None or not formula:
        print("Incorrect formula")
        formula = input("Enter the logic formula:\n")
        formula = formula.strip()
    node = Node()
    if not node.parse(formula):
        print("Unsuccessful parsing!")
    else:
        print("Successful parsing!")

except Exception as ex:
    print("OMG, it is unknown error!")
    print(ex)
    exit()



