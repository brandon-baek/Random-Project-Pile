from math import factorial as f
from os import system as sys
from random import randint

while True:
    sys('clear')
    ids = set()
    length = 0
    amount = 0
    first = True

    while not length or 10 ** length < amount:
        if not first:
            print("\nError: The total combinations possible with the "
                  "length provided is less than the amount requested."
                  f" Max length: ({10 ** length})\n")
        length = int(input('Length of ID? '))
        amount = int(input('How many IDs? '))
        first = False

    while len(ids) != amount:
        code = ""
        for _ in range(length):
            code += str(randint(0, 9))
        ids.add(code)
        sys('clear')
        print(f'[{int((len(ids) / amount) * 100)}%] Complete')

    print('\n\nIDS:\n')

    for i in ids:
        print(i)

    input("\n\nEnter anything to restart")