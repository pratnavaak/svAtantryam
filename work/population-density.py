file = [line.split(',') for line in open('population-density.csv').read().split('\n') if line][1:]

file = [line for line in file if len(line) > 3 and line[1]]

data = {}
name = {}

for line in file:
    data.setdefault(line[1], {})[int(line[2])] = float(line[3])
    name[line[1]] = line[0]

ref = 1800

def before(country):
    b = [data[country][y] for y in data[country].keys() if y < ref]
    if not b:
        print(name[country])
        return min(data[country][y] for y in data[country].keys())
    return max(b)

def latest(country):
    return data[country][2024]

lbr = sorted([[c, name[c], before(c), latest(c), latest(c) / before(c)] for c in data.keys()], key = lambda x: x[4])

#print(lbr[:10])

with open('lbr.csv','w+') as f:
    f.write(f'country code,country name,max population density before {ref} (or min of dataset if not available before {ref}),current population density,ratio\n')
    f.write('\n'.join([','.join([str(v) for v in c]) for c in lbr]))