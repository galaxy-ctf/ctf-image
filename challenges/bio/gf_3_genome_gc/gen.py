import random
import sys
import uuid

flag='GCCCTF F571A37E-1352-488D-9C13-0F6663FE53BA '

def calc(data):
    G = data.count('G')
    C = data.count('C')
    return int(100 * (G + C)/float(len(data)))


def find(target_value):
    initial_string = [random.choice(list('ACTG')) for _ in range(100)]
    while True:
        current = calc(initial_string)
        if current == target_value:
            return ''.join(initial_string)
        elif current < target_value:
            initial_string[random.choice(range(len(initial_string)))] = random.choice(list('GC'))
        elif current > target_value:
            initial_string[random.choice(range(len(initial_string)))] = random.choice(list('AT'))


for c in list(flag):
    sys.stdout.write('>')
    sys.stdout.write(uuid.uuid4().hex)
    sys.stdout.write('\n')
    sys.stdout.write(find(ord(c)))
    sys.stdout.write('\n')
