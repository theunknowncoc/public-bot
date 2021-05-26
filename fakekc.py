import random


def fakekc():
    lst = []
    with open('phones.txt', 'r') as f:
        z = f.read().split('\n')
        z = z[:-1]
    dev = []
    for i in range(random.randint(2, 6)):
        dev.append(random.choice(z))

    year = random.randint(2013, 2018)
    chars = [chr(i) for i in range(48, 123) if i not in list(
        range(58, 65)) and i not in list(range(91, 97))]
    nc = ''
    case = random.randint(1, 2)
    names = []

    for j in range(random.randint(0, 3)):
        name = ''
        for i in range(random.randint(3, 15)):
            name += random.choice(chars)
        names.append(name)
    kc = 'Devices: '
    for i in dev:
        kc += i + ' '
    kc += '\n\nYear Made: '+str(year)+'\n'
    if len(names) > 0:
        kc += '\nOld Names: '
        for i in names[:-1]:
            kc += i + ' & '
        kc += names[-1]
    return kc
