"""Node - an object of a parsed logical formula, a semantic tree.

Author - Yegor Ryazantsev"""


from string import ascii_letters
import re


class Node:
    dis = {'+', '|'}
    con = {'*', '&'}
    type = None
    left = None
    right = None

    def __getbrackets(self, local_form):
        result = []
        right_brackets = 0
        local_result = []
        for i in range(0, len(local_form)):
            if local_form[i] == '(' and right_brackets == 0:
                local_result.append(i)
                right_brackets += 1
            elif local_form[i] == '(':
                right_brackets += 1
            elif local_form[i] == ')' and right_brackets == 1:
                local_result.append(i)
                result.append(local_result)
                local_result = []
                right_brackets -= 1
            elif local_form[i] == ')' and right_brackets > 1:
                right_brackets -= 1
            elif local_form[i] == ')' and right_brackets == 0:
                return None
        if right_brackets != 0:
            return None
        return result

    def parse(self, formula):

        """Create the object with parsing of logical formula.

        Params:
        formula - str, the formula.
        Returns:
        True, if parsing is successful and the formula is correct; else, False.
        """


        formula = formula.strip()
        brackets = []
        while True:
            # 0. Если строка пустая
            if re.search("[^01\+|\*&()\-a-zA-Z\s=>]", formula) != None or not formula:
                return False
            # 1. Если справа или слева - +|*& или - справа то ошибка
            if formula[0] in self.dis or formula[0] in self.con:
                return False
            if formula[-1] in self.dis or formula[-1] in self.con or formula[-1] == '-':
                return False
            brackets = self.__getbrackets(formula)
            if brackets is None:
                return False
            if len(brackets) == 1 and brackets[0] == [0, len(formula) - 1]:
                formula = formula[1:-1].strip()
            else:
                break

        def out_of(bracket_range, length):
            i = length - 1
            if len(bracket_range) == 0:
                while i >= 0:
                    yield i
                    i -= 1
            else:
                flag = len(bracket_range) - 1
                while i >= 0:
                    if flag < 0 or i > bracket_range[flag][1]:
                        yield i
                        i -= 1
                    else:
                        i = bracket_range[flag][0] - 1
                        flag -= 1

        priority = {'=': 0, '>': 1, '+': 2, '|': 2, '*': 3, '&': 3, '-': 4}
        found = -1
        present_priority = 5
        for i in out_of(brackets, len(formula)):
            if priority.get(formula[i], 5) < present_priority:
                found = i
                present_priority = priority.get(formula[i], 5)

        if found == -1:
            if len(formula) > 1:
                return False
            else:
                self.type = formula
                return True
        else:
            if formula[found] == '-':
                if found != 0:
                    return False
                else:
                    self.type = '-'
                    self.right = Node()
                    return self.right.parse(formula[1:])
            else:
                self.type = formula[found]
                self.left = Node()
                self.right = Node()
                return self.left.parse(formula[:found]) and self.right.parse(formula[found + 1:])

    def calc(self, **args):

        """Calculate the logical value of the logical formula.

        Params:
        **args - values of logical variables.
        Returns:
        The logical value of the formula or None if the formula isn't correct."""

        if self.type == '-':
            answer = self.right.calc(**args)
            if answer is None:
                return None
            return not answer
        if self.type in self.con:
            answer1 = self.left.calc(**args)
            answer2 = self.right.calc(**args)
            if answer1 is None or answer2 is None:
                return None
            return answer1 and answer2
        if self.type in self.dis:
            answer1 = self.left.calc(**args)
            answer2 = self.right.calc(**args)
            if answer1 is None or answer2 is None:
                return None
            return answer1 or answer2
        if self.type == '>':
            answer1 = self.left.calc(**args)
            answer2 = self.right.calc(**args)
            if answer1 is None or answer2 is None:
                return None
            return not answer1 or answer2
        if self.type == '=':
            answer1 = self.left.calc(**args)
            answer2 = self.right.calc(**args)
            if answer1 is None or answer2 is None:
                return None
            return (answer1 and answer2) or (not answer1 and not answer2)
        if self.type == '1':
            return True
        if self.type == '0':
            return False
        if self.type in ascii_letters:
            return args.get(self.type, None)

    def args(self):

        """Returns a set of names of the variables of the formula."""

        try:
            if self.type in ascii_letters:
                return {self.type}
            if self.type == '-' and self.right is not None:
                return self.right.args()
            if self.type in {'=', '>', '+', '|', '*', '&'} and self.left is not None and self.right is not None:
                return self.left.args() | self.right.args()
            if self.type in {'1', '0'}:
                return {}
        except TypeError:
            return None