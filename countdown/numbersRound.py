'''
from the game countdown: receive 6 ints and a target int.
it must be reached with + * / -
'''

import random
import time

below_zeros_allowed = False
game_time_limit = 30


class Stopper:
    def __init__(self, int):
        self.stop_at = int


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
                 number_node=True, parent=None, distance=0, stopper=None):
        self.parent = parent
        self.val = str(root_value)
        self.remainingArray = remaining_array
        self.numberNode = number_node
        self.children = []
        self.distance = distance
        self.target = target
        self.stopper = stopper

    def __str__(self):
        string = (self.distance * ". ") + str(self.val)
        if len(self.children) > 0:
            string += ": "
            for child in self.children:
                string += "\n" + str(child)
        return string

    def addChild(self, val):
        self.children.append(val)

    def populate_tree(self):
        global below_zeros_allowed
        if self.target is None:
            self.stopper.stop_at = self.stopper.stop_at - 1

        if len(self.remainingArray) == 0 and self.numberNode:
            self.result = self.get_result()
            self.children = [self.result]

            if self.target is not None:
                if float(self.result).is_integer() and int(self.result) == self.target:
                    return self.get_result_string()

            else:
                if self.stopper.stop_at <= 0 and float(self.result).is_integer():
                    if below_zeros_allowed:
                        return self.result, self.get_result_string()
                    elif self.result >= 0:
                        return self.result, self.get_result_string()

        elif self.numberNode:
            for operator in self.operators:
                self.addChild(SumTree(operator, self.remainingArray, number_node=False, target=self.target, parent=self,
                                      distance=self.distance + 1, stopper=self.stopper))

        else:
            for remainer in self.remainingArray:
                remainers = self.remainingArray.copy()
                remainers.remove(remainer)

                self.addChild(SumTree(remainer, remainers, target=self.target, parent=self, distance=self.distance + 1,
                                      stopper=self.stopper))

    def recursivePop(self):
        result = self.populate_tree()
        if result is not None:
            return result
        if len(self.remainingArray) > 0:
            for child in self.children:
                result = child.recursivePop()
                if result is not None:
                    return result

    def get_result(self):
        return eval(self.get_result_string())

    def get_result_string(self):
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

        return s


def find_permutation(arr, objective=None):
    answer = None
    tree = None

    if objective is None:
        first_entry = random.randint(0, len(arr) - 1)
        stop_at = Stopper(random.randint(0, 200000))

    for i in range(len(arr)):
        remaining_array = []
        remaining_array.extend(arr[:i])
        remaining_array.extend(arr[i + 1:])

        if objective is None:
            if i != first_entry:
                continue
            tree = SumTree(root_value=arr[i], remaining_array=remaining_array, stopper=stop_at)

        else:
            tree = SumTree(root_value=arr[i], remaining_array=remaining_array, target=objective)

        answer = tree.recursivePop()

        if answer is not None:
            break

    if objective is None and tree is not None:
        return answer

    if answer is not None and tree is not None:
        print("********************************")
        print("solution found: ")
        print(answer + " = " + str(tree.target))
    else:
        print("No combination of all inputs %a found that results in %d" % (arr, objective))

    return answer


def random_big():
    return random.randint(2, 10) * 10


def random_small():
    return random.randint(1, 9)


def get_random_numbers(b):
    total = 6
    s = total - b

    smalls = []
    for i in range(s):
        smalls.append(random_small())

    bigs = []
    for i in range(b):
        bigs.append(random_big())

    all_randoms = []
    all_randoms.extend(bigs)
    all_randoms.extend(smalls)
    return all_randoms


def main():
    number_of_bigs = 2
    arr = get_random_numbers(number_of_bigs)
    print("array is " + str(arr))

    answer = find_permutation(arr)
    print("score to find: " + str(answer[0]))

    time.sleep(2)

    print("you have %d seconds!" % game_time_limit)

    for i in range(game_time_limit, 0, -1):
        print("%d seconds left" % i)
        time.sleep(1)

    print("time's up!")
    time.sleep(2)
    print("did you get it?")
    time.sleep(2)
    print("the answer was of course " + str(answer[1]) + " = " + str(answer[0]) + " !")

    time.sleep(2)

    a = input("Do you want to play again (with different numbers)? [Y/n]\n")

    if a == 'y' or a == 'y':
        main()
    else:
        print("bye bye!")
        exit(0)


main()
