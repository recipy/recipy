import pandas as pd
from matplotlib.pyplot import *

data = pd.read_csv('data.csv')

data.plot(x='year', y='temperature')
savefig('plot.png')