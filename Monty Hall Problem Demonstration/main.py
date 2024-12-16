from random import choice, randint, shuffle, seed


set_seed = 1
epochs = 10000000

def monty_hall_simulation_switch():
    doors = [0, 0, 1]
    shuffle(doors)

    initial_choice = randint(0, 2)
    initial_choice_prize = doors[initial_choice]

    # Host opens a door with a goat, but it's not the initially chosen door
    available_doors = [i for i in range(3) if i != initial_choice and doors[i] == 0]
    host_reveal = choice(available_doors)

    # Determine the other door that the contestant can switch to
    switch_choice = next(i for i in range(3) if i not in (initial_choice, host_reveal))

    # To simulate switching, we check the switch choice
    return doors[switch_choice] == 1  # Return True if switching wins the car

def monty_hall_simulation_stick():
    doors = [0, 0, 1]
    shuffle(doors)

    initial_choice = randint(0, 2)

    # To simulate sticking, we check the initial choice
    return doors[initial_choice] == 1  # Return True if sticking wins the car

def monty_hall_simulation_random():
    doors = [0, 0, 1]
    shuffle(doors)

    initial_choice = randint(0, 2)
    initial_choice_prize = doors[initial_choice]

    # Host opens a door with a goat, but it's not the initially chosen door
    available_doors = [i for i in range(3) if i != initial_choice and doors[i] == 0]
    host_reveal = choice(available_doors)

    # Randomly decide whether to stick with the initial choice or switch
    if choice([True, False]):
        # Stick with the initial choice
        return doors[initial_choice] == 1
    else:
        # Switch to the other door
        switch_choice = next(i for i in range(3) if i not in (initial_choice, host_reveal))
        return doors[switch_choice] == 1

seed(set_seed)
attempts_switch = [monty_hall_simulation_switch() for _ in range(epochs)]

seed(set_seed)
attempts_stick = [monty_hall_simulation_stick() for _ in range(epochs)]

seed(set_seed)
attempts_random = [monty_hall_simulation_random() for _ in range(epochs)]


print("Wins by switching:", attempts_switch.count(True))

print("Losses by switching:", attempts_switch.count(False))

print()

print(f'{attempts_switch.count(True) / len(attempts_switch) * 100}% Win by switching')

print(f'{attempts_switch.count(False) / len(attempts_switch) * 100}% Loss by switching')

print('\n')

print("Wins by sticking:", attempts_stick.count(True))

print("Losses by sticking:", attempts_stick.count(False))

print()

print(f'{attempts_stick.count(True) / len(attempts_stick) * 100}% Win by sticking')

print(f'{attempts_stick.count(False) / len(attempts_stick) * 100}% Loss by sticking')

print('\n')

print("Wins by random choice:", attempts_random.count(True))

print("Losses by random choice:", attempts_random.count(False))

print()

print(f'{attempts_random.count(True) / len(attempts_random) * 100}% Win by random choice')

print(f'{attempts_random.count(False) / len(attempts_random) * 100}% Loss by random choice')
