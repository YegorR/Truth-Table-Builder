"""TruthTableBuilder creates a truth table of user's logical expression.

Input - a logical formula with symbols:
    '1', '0' - 'truth' and 'false' respectively;
    '+', '|' - disjunction;
    '*', '&' - conjunction;
    '-' - inversion;
    '>' - implication
    '=' - equality;
    latin symbols - logic variables(the register matters).
Output - a truth table.
For examples:
Input: a > b * c
Output:
    a	b	c	F
    0	0	0	1
    1	0	0	0
    0	1	0	1
    1	1	0	0
    0	0	1	1
    1	0	1	0
    0	1	1	1
    1	1	1	1
If the formula is incorrect, program prints : "The incorrect formula!" and ends.
Author - Yegor Ryazantsev.
"""

from Node import *

try:
    formula = input("Enter the logic formula:\n")
    node = Node()
    if not node.parse(formula):
        print("The incorrect formula!")
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
    print("Oh, it is unknown error!")
    print(ex)
    exit()



