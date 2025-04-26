import random

def genRanStr (length):
    characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    string = ''

    for i in range(len(characters)):
        string += str(random.choice(characters))

    return string