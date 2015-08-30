import sys
import os
sys.path.insert(0, os.path.abspath('../'))

import recipy
import numpy

arr = numpy.arange(10)
arr = arr + 500
# We've made a fairly big change here!

numpy.save('simple_test.npy', arr)
