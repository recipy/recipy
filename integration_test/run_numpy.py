import recipy
import numpy as np
import sys
in_file=sys.argv[1]
out_file=sys.argv[2]
data = np.loadtxt(in_file, delimiter=',')
np.savetxt(out_file, data, delimiter=',')
