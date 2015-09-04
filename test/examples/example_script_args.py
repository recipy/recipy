import recipy

import sys
import numpy as np

start = int(sys.argv[1])
end = int(sys.argv[2])

arr = np.arange(start, end)

np.save('range.npy', arr)
