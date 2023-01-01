from random import *
import csv
from statistics import NormalDist

def roll(n):
    result = randint(1, n)
    print("Rolled", result, "out of", n)
    return result

def rolp(n):
    result = 0
    while True:
        p = roll(n)
        result += p
        if p != n:
            break
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

jakar = '“Mumbling” Jakar Mer M/Baparan Q1 Merchant QIx1'
