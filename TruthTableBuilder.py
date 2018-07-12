# На вход подаётся формула, которая включает в себя:
# латинские буквы, символы 1 и 0, + или |, * или &, -, (), =, >
# используется регуларное выражение [^01\+|\*&()\-a-zA-Z\s=>]
from Node import *

try:
    formula = input("Enter the logic formula:\n")
    node = Node()
    if not node.parse(formula):
        print("Incorrect formulaS!")
        exit()

    args = list(node.args())
    args.sort()
    for i in args:
        print(i, end='\t')
    print('F')
    for i in range(0, 2**len(args)):
        values = []
        for j in range(0, len(args)):
            if i // 2**j % 2 == 1:
                values.append(True)
                print(1, end='\t')
            else:
                values.append(False)
                print(0, end='\t')
        if node.calc(**dict(zip(args, values))):
            print(1)
        else:
            print(0)




except Exception as ex:
    print("OMG, it is unknown error!")
    print(ex)
    exit()



