import recipy
import pandas as pd
from matplotlib.pyplot import *

data = pd.read_csv('data.csv')

data.plot(x='year', y='temperature')
savefig('newplot.pdf')

data.temperature = data.temperature * 100
data.to_csv('output2.csv')