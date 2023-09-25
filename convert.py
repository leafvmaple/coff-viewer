import csv

path = input()
key = input()
value = input()

res = []
with open(path, 'r') as f:
    reader = csv.DictReader(f)
    for line in reader:
        if line[value] == '' or line[value] == 'Reserved for future use.':
            continue

        print('"%s": "%s",' % (line[key], line[value]))
