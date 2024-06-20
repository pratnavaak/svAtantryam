from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import math

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
    return data[country][min(data[country].keys(), key = lambda k: abs(k - datetime.now().year))]

lbr = sorted([[c, name[c], before(c), latest(c), latest(c) / before(c)] for c in data.keys()], key = lambda x: x[4])

#print(lbr[:10])

with open('lbr.csv','w+') as f:
    f.write(f'country code,country name,max population density before {ref} (or min of dataset if not available before {ref}),current population density,ratio\n')
    f.write('\n'.join([','.join([str(v) for v in c]) for c in lbr]))


years = [str(y) for y in range(2018, 2024)]

maxr = max([l[4] for l in lbr])
tickvals = [1,10,100,1000,6000]

fig = go.Figure(data=go.Choropleth(
    locations = [l[0] for l in lbr],
    z = [math.log(l[4]) for l in lbr],
    text = [l[0] for l in lbr],
        showscale=True,
        colorscale = 'Turbo',
        colorbar=dict(
            tickvals = [math.log(v) for v in tickvals],
            ticktext = tickvals,
        ),
        hovertext=[str(l[4]) for l in lbr],
        marker_line_color='black',
        marker_line_width=0.1,
    ), layout=go.Layout(title = "industrial revolution effect: current population / max population before 1800"))

fig.update_geos(
    showcountries=True,
    projection_type="miller"
)

fig.show()

#fig.write_image('population-density-capacity.png')