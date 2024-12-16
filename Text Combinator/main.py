from itertools import product
from string import ascii_lowercase
import threading
import time

def infinite_combinations():
    alphabet = ascii_lowercase + ' '
    length = 1
    while True:
        for combination in product(alphabet, repeat=length):
            yield ''.join(combination)
        length += 1

def print_guesses():
    global guess, history
    while True:
        if len(history) > 0:
            print(history[-1])
        else:
            time.sleep(0.01)  # Sleep for a short while to avoid busy waiting

generator = infinite_combinations()

answer = 'how t'
guess = ''
history = []

# Start the printing thread
printing_thread = threading.Thread(target=print_guesses)
printing_thread.daemon = True  # Set as daemon so it stops when the main thread stops
printing_thread.start()

while guess != answer:
    guess = next(generator)
    history.append(guess)

edit_length = 2

edited_history = [i for i in history if len(i) == edit_length]

print(len(edited_history))
print(len(history))

percentage = (len(edited_history) / len(history)) * 100
percentage = round(percentage, 2) if str(percentage)[0] != '0' else percentage
percentage = int(percentage) if str(percentage)[-1] == '0' and str(percentage)[-2] == '.' else percentage

print(f'Length of {edit_length} is {percentage}% of history')
