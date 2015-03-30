import recipy
import numpy as np

arr = np.arange(10)
arr = arr + 5

np.save('test2.npy', arr)