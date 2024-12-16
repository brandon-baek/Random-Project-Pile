import shelve
from os import system as sys

rand_seed_db = shelve.open('RAND_SEED')

class XORShiftRandom:
    def __init__(self, seed):
        self.state = seed

    def next(self):
        x = self.state
        x ^= x << 13
        x ^= x >> 17
        x ^= x << 5
        self.state = x
        y = x & 0xFFFFFFFF
        rand_seed_db['seed'] = y
        return y

def get_random():
    try:
        random = XORShiftRandom(rand_seed_db['seed'])
    except:
        rand_seed_db['seed'] = 120413948082395710539
        random = XORShiftRandom(rand_seed_db['seed'])
    return random.next()

received_randoms = []
got_random = 0

while got_random not in received_randoms:
    received_randoms.append(got_random)
    got_random = get_random()
    sys('clear')
    print(received_randoms)


print(received_randoms)