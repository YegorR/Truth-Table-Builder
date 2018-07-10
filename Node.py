class Node:
    nodeType = {'Letter': 0, 'True': 1, 'False': 2, 'Tree': 3}
    dis = {'+', '|'}
    con = {'*', '&'}
    type = None
    left = None
    right = None

    def __init__(self, local_form):
        local_form = local_form.strip()
        while True:
            # 0. Если строка пустая
            if not local_form:
                return False
            # 1. Если справа или слева - +|*& или - справа то ошибка
            if local_form[0] in self.dis or local_form[0] in self.con:
                return False
            if local_form[-1] in self.dis or local_form[-1] in self.con or local_form[-1] == '-':
                return False
            else:
                break
        brackets = self.__brackets(local_form)
        print(brackets)  # Проверка, работают ли скобки адекватно

    def __brackets(self, local_form):
        result = []
        rightBrackets = 0
        local_result = []
        for i in range(0, len(local_form)):
            if local_form[i] == '(' and rightBrackets == 0:
                local_result.append(i)
                rightBrackets += 1
            elif local_form[i] =='(':
                rightBrackets +=1
            elif local_form[i] == ')' and rightBrackets == 1:
                local_result.append(i)
                result.append(local_result)
                local_result = []
                rightBrackets -= 1
            elif local_form[i] == ')' and rightBrackets > 1:
                rightBrackets -= 1
            elif local_form[i] == ')' and rightBrackets == 0:
                return None
        if rightBrackets != 0:
            return None
        return result