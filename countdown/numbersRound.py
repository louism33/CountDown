'''
from the game countdown: receive 6 ints and a target int.
it must be reached with + * / -
'''

class SumTree:
    plus = "+"
    minus = "-"
    times = "*"
    div = "/"
    operators = []
    operators.append(plus)
    operators.append(minus)
    operators.append(times)
    operators.append(div)

    def __init__(self, root_value, remaining_array=[], target=None,
                 number_node=True, parent=None, distance=0):

        self.parent = parent
        self.val = str(root_value)
        self.remainingArray = remaining_array
        self.numberNode = number_node
        self.children = []
        self.distance = distance
        self.target = target

    def __str__(self):
        string = (self.distance * ". ") + str(self.val)
        if len(self.children) > 0:
            string += ": "
            for child in self.children:
                string += "\n" + str(child)
        return string

    def addChild(self, val):
        self.children.append(val)

    def populateTree(self):
        if len(self.remainingArray) == 0 and self.numberNode:
            self.result = self.getResult()
            self.children = [self.result]

            if self.target is not None:
                if int(self.result) == self.target:
                    # print("VICTORYYY")
                    # print("target: " + str(self.target) + ", res: " + str(self.result))
                    return self.getResultString()

        elif self.numberNode:
            for operator in self.operators:
                self.addChild(SumTree(operator, self.remainingArray, number_node=False, target=self.target, parent=self, distance=self.distance + 1))

        else:
            for remainer in self.remainingArray:
                remainers = self.remainingArray.copy()
                remainers.remove(remainer)
                self.addChild(SumTree(remainer, remainers, target=self.target, parent=self, distance=self.distance + 1))

    def recursivePop(self):
        result = self.populateTree()
        if result is not None:
            return result
        if len(self.remainingArray) > 0:
            for child in self.children:
                result = child.recursivePop()
                if result is not None:
                    return result

    def getResult(self):
        return eval(self.getResultString())

    def getResultString(self):
        node = self
        a = []
        while node.parent is not None:
            a.append(str(node.val))
            node = node.parent

        a.append(node.val)
        a = a[::-1]

        starter_brackets = []
        if len(a) > 3:
            length = len(a[3:])
            b = []
            starter_brackets.append("(")
            b.extend(a[0:3])
            b.append(")")
            for i in range(length, 0, -2):
                starter_brackets.append("(")
                b.extend(a[i + 1:i + 3])
                b.append(")")
            a = b

        s = "".join(x for x in a)
        s = "".join(x for x in starter_brackets) + s

        # print(s)

        return s


# arr = [100, 1, 2, 3, 4, 5]
arr = [100, 1, 2, 3, 4, 5, 6]
objective = 102

# print("**************************")
tree = SumTree(root_value=arr[0], remaining_array=arr[1:], target=objective)
answer = tree.recursivePop()
# print("**************************")
# print(tree)

if answer is not None:
    print("********************************")
    print("solution found: ")
    print(answer + " = " + str(tree.target))
else:
    print("No combination of all inputs %a found that results in %d" % (arr, objective))
