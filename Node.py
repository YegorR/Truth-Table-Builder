class Node:
    nodeType = {'Letter': 0, 'True': 1, 'False': 2, 'Tree': 3}
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

    def parse(self, local_form):
        local_form = local_form.strip()
        brackets = []
        while True:
            # 0. Если строка пустая
            if not local_form:
                return False
            # 1. Если справа или слева - +|*& или - справа то ошибка
            if local_form[0] in self.dis or local_form[0] in self.con:
                return False
            if local_form[-1] in self.dis or local_form[-1] in self.con or local_form[-1] == '-':
                return False
            brackets = self.__getbrackets(local_form)
            if brackets is None:
                return False
            if len(brackets) == 1 and brackets[0] == [0, len(local_form)-1]:
                local_form = local_form[1:-1].strip()
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
        for i in out_of(brackets, len(local_form)):
            if priority.get(local_form[i], 5) < present_priority:
                found = i
                present_priority = priority.get(local_form[i], 5)

        if found == -1:
            if len(local_form) > 1:
                return False
            else:
                type = local_form
                return True
        else:
            if local_form[found] == '-':
                if found != 0:
                    return False
                else:
                    type = '-'
                    right = Node()
                    return right.parse(local_form[1:])
            else:
                type = local_form[found]
                left = Node()
                right = Node()
                return left.parse(local_form[:found]) and right.parse(local_form[found+1:])
        return True