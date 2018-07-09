#На вход подаётся формула, которая включает в себя:
#латинские буквы, символы 1 и 0, + или |, * или &, -, ()
#используется регуларное выражение [^01\+|\*&()\-a-zA-Z\s]
import re

try:
    formula = input("Enter the logic formula:\n")
    formula = formula.strip()
    while re.search("[^01\+|\*&()\-a-zA-Z\s]", formula)!=None or not formula:
        print("Incorrect formula")
        formula = input("Enter the logic fornula:\n")
        formula = formula.strip()
except:
    print("OMG, it is unknown error")
    exit()
