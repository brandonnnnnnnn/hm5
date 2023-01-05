from random import *
import csv
# import pandas as pd
from statistics import NormalDist
import itertools

def roll(n):
    result = randint(1, n)
    print("Rolled", result, "out of", n)
    return result

def rolp(n):
    result = 0
    curr = roll(n)
    while curr == n:
        result += curr - 1
        curr = roll(n)
    result += curr
    return result

def randstat(mean, sd):
    # percentile = mean + z * stdev
    thing = NormalDist(mean, sd)
    percentile = randint(0, 999) / 1000
    print("percentile", percentile)
    return thing.inv_cdf(percentile)

def randchar(race):
    if race[0] == 'm':
        if race[1] == 'Brandobian':
            mean = 69
            sd = 2.92
    if race[0] == 'f':
        if race[1] == 'Brandobian':
            mean = 63.7
            sd = 2.8
    print(randstat(mean,sd))

# America M: 5'9.3", SD 2.92 F: 5'3.8", SD 2.8
# Canada M: 5'8.9", F: 5'3.9"
# Chile M: 5'7.4", F: 5'1.9"
# China M: 5'5.8", SD 2.92 F: 5'1.3", SD 2.8
# Denmark M: 5'11" F: 5'5.8"
# Ethiopia M: 5'7" F: 5'2"
# Taiwawn M: 5'7.5", F: 5'3"
#  UK M: 5'9" F: 5'3.7"

# Brandobia - uk (69, 2.92), (63.7, 2.8)
# Deji - chile
# Fhokki - denmark
# Kalamaran - america
# Reanaarian - taiwan
# Svimohz - ethiopia

def writeTowns():
    o = open('towns.txt')
    reader = o.readlines()
    c = open('towns.csv', 'w', newline='')
    writer = csv.DictWriter(c, ['name','population','country','page','latitude','longitude'])
    writer.writeheader()
    for line in reader:
        print(line)
        csvline = str2csv(line)
        writer.writerow(csvline)
        print(csvline)

def str2csv(stri):
    csv = {}
    i = stri.split(' ')
    # population = i[-5]
    # country = i[-4]
    page = i[-3]
    latitude = i[-2]
    longitude = i[-1]
    if i[-5][0].isdigit() or i[-5] == 'RUINS':
        country = i[-4]
        population = i[-5]
    else: 
        country = i[-5] + ' ' + i[-4]
        population = i[-6]
    name = stri.split(' ' + population)[0]
    csv['name'] = name
    csv['population'] = population
    csv['country'] = country
    csv['page'] = page
    csv['latitude'] = latitude
    csv['longitude'] = longitude.strip('\n')
    return csv

def charinfo(lnum):
    with open('chars.csv') as f:
        return next(itertools.islice(csv.DictReader(f), lnum - 2, None))

def towninfo(lnum):
    with open('towns.csv') as f:
        return next(itertools.islice(csv.DictReader(f),lnum-2,None))

def info(lnum):
    with open('info.csv') as f:
        return next(itertools.islice(csv.DictReader(f),lnum-2,None))

def mobinfo(lnum):
    with open('mobs.csv') as f:
        return next(itertools.islice(csv.DictReader(f),lnum-2,None))

def fightinfo(lnum):
    with open('battle.csv') as f:
        return next(itertools.islice(csv.DictReader(f),lnum-2,None))

def arena():
    clock = 0
    spawn(33)
    alive = True
    playerInit = input("Player init roll (d12): ")
    enemy = 4
    while alive:
        if clock % 30 == 0:
            enemy += rolp(8) - 2
            spawn(enemy)
            # while True:
            #     try:
            #         spawn(enemy)
            #         print(mobinfo(enemy)['Name'],"has joined the battle!")
            #         break
            #     except:
            #         input("Info missing for "+mobinfo(enemy)+'. Please enter info and try again')
        clock += 1
        print("count:",clock)
        action = input("Player's action (enter=continue, f=fight, m=move, end=end simulation): ")
        if action == 'm':
            print('current position:',fightinfo(2)['x'],fightinfo(2)['y'])
        if action == 'end':
            print('Good game!')
            with open('battle.csv','r+') as f:
                f.readline() # save header
                f.truncate(f.tell()) # clear all combatants
            return

def spawn(mobid):
    info = mobinfo(mobid)
    char = {}
    char['type'] = info['Name']
    while True:
        try:
            if info['HP'] == None: raise Exception
            break
        except:
            print("HP info missing for "+char['type']+'. Please enter info and try again')
            input("Press enter when ready: ")
            info = mobinfo(mobid)
    char['maxhp'] = str2roll(info['HP'])
    print(char['maxhp'])
    char['hp'] = char['maxhp']
    char['natreach'] = info['Reach']
    x=0
    y=0
    while (x not in [1,8]) and (y not in [1,16]):    
        x = randint(1,8)
        y = randint(1,16)
    char['x'] = x
    char['y'] = y
    char['momentum'] = 1
    print(char)
    print(info['Name'],"spawned at x:",x,'y:',y,'!')
    fields = ['type','maxhp','hp','wounds','armor','natreach','lh','rh','x','y','momentum']
    w = open('battle.csv','a',newline='')
    writer = csv.DictWriter(w,fields)
    writer.writerow(char)

def str2roll(string):
    print('hit dice:',string)
    parts = string.split('+')
    total = 0
    for part in parts:
        if 'd' not in part: total += int(part)
        else:
            if part[0] == 'd': 
                total += roll(int(part[1:]))
                continue
            comps = part.split('d')
            for i in range(int(comps[0])):
                if 'p' not in comps[1]:
                    total += roll(int(comps[1]))
    return total