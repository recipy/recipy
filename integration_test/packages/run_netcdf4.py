"""
Sample script that runs netcdf4 functions logged by recipy.
"""

# Copyright (c) 2016, 2018 University of Edinburgh and Netherlands eScience
# Center

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)
import recipy

import os
import sys
import netCDF4

from integration_test.packages.base import Base


class NetCDF4Sample(Base):
    """
    Sample script that runs netcdf4 functions logged by recipy.

    This class assumes the existence of a data/netcdf4 directory,
    co-located with this file, with the following content:

    * testrh.nc: test netcdf file (taken from
      https://www.unidata.ucar.edu/software/netcdf/examples/files.html)
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "netcdf4")

    def dataset_read(self):
        """
        Use Dataset to read netcdf file.
        """
        file_name = os.path.join(self.data_dir, "testrh.nc")
        netCDF4.Dataset(file_name)

    def dataset_write(self):
        """
        Use Dataset to write netcdf file.
        """
        file_name = os.path.join(self.data_dir, "data.nc")
        netCDF4.Dataset(file_name, mode='w')
        os.remove(file_name)

    def dataset_append(self):
        """
        Use Dataset to append to netcdf file.
        """
        file_name = os.path.join(self.data_dir, "testrh.nc")
        netCDF4.Dataset(file_name, mode='a')


if __name__ == "__main__":
    NetCDF4Sample().invoke(sys.argv)
