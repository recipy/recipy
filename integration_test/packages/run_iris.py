"""
Sample script that runs iris functions logged by recipy.
"""

# Copyright (c) 2016, 2018 University of Edinburgh and Netherlands eScience
# Center

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)
import recipy

import os
import sys
import iris
import numpy as np

from integration_test.packages.base import Base


class IrisSample(Base):
    """
    Sample script that runs iris functions logged by recipy.

    This class assumes the existence of a data/iris directory,
    co-located with this file, with the following content:

    * cube1.nc: netCDF file containing a single iris cube.
    * cube2.nc: netCDF file containing a single iris cube.

    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "iris")

    def load(self):
        """
        Use iris.load to read a netcdf file.
        """
        file_name = os.path.join(self.data_dir, "cube1.nc")
        iris.load(file_name)

    def load_list(self):
        """
        Use iris.load to read a list of netcdf files.
        """
        file_names = ['cube1.nc', 'cube2.nc']
        file_names = [os.path.join(self.data_dir, f) for f in file_names]

        iris.load(file_names)

    def load_glob(self):
        """
        Use iris.load to read a list of netcdf files based on a glob pattern.
        """
        file_name = os.path.join(self.data_dir, "cube*.nc")
        iris.load(file_name)

    def load_cube(self):
        """
        Use iris.load_cube to read a netcdf file.
        """
        file_name = os.path.join(self.data_dir, "cube1.nc")
        iris.load_cube(file_name)

    def load_cubes(self):
        """
        Use iris.load_cubes to read multiple netcdf files.
        """
        file_names = ['cube1.nc', 'cube2.nc']
        file_names = [os.path.join(self.data_dir, f) for f in file_names]

        iris.load_cubes(file_names, ['air_temperature', 'water_temperature'])

    def load_raw(self):
        """
        Use iris.load_raw to read a netcdf file.
        """
        file_name = os.path.join(self.data_dir, "cube1.nc")
        iris.load_raw(file_name)

    def save(self):
        """
        Use iris.save to save data to a netcdf file.
        """
        cube = iris.cube.Cube(data=np.random.randn(2, 3))

        file_name = os.path.join(self.data_dir, "cube.nc")
        iris.save(cube, file_name)

        os.remove(file_name)


if __name__ == "__main__":
    IrisSample().invoke(sys.argv)
