"""
Usage: python -m recipy example_script3.py OUTPUT.npy
"""

from __future__ import print_function
import sys

import numpy

if len(sys.argv) < 2:
    print(__doc__, file=sys.stderr)
    sys.exit(1)

arr = numpy.arange(10)
arr = arr + 500
# We've made a fairly big change here!

numpy.save(sys.argv[1], arr)
