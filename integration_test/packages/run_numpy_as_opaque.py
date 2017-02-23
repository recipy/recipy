"""
Sample script that runs numpy functions logged by recipy, when
imported as aliases.
"""

# Copyright (c) 2016 University of Edinburgh.

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import recipy

import os
import sys
import numpy as opaque
from numpy import savetxt as cryptic

from integration_test.packages.base import Base


class NumpyAsOpaqueSample(Base):
    """
    Sample script that runs numpy functions logged by recipy,
    when imported as aliases.

    All functions that save files delete the files after saving,
    to keep the directory clean.
    """

    def __init__(self):
        """
        Constructor.
        """
        Base.__init__(self)

    def opaque_savetxt(self):
        """
        Use numpy.savetxt to save a file out.txt.
        """
        file_name = os.path.join(self.current_dir, "out.txt")
        data = opaque.arange(10)
        opaque.savetxt(file_name, data)
        os.remove(file_name)

    def cryptic(self):
        """
        Use numpy.savetxt to save a file out.txt.
        """
        file_name = os.path.join(self.current_dir, "out.txt")
        data = opaque.arange(10)
        cryptic(file_name, data)
        os.remove(file_name)

if __name__ == "__main__":
    NumpyAsOpaqueSample().invoke(sys.argv)
