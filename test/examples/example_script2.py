import recipy
import numpy

arr = numpy.arange(10)
arr = arr + 500
# We've made a fairly big change here!

numpy.save('testNGCM_2.npy', arr)
