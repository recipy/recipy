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
import xarray
import numpy as np

from integration_test.packages.base import Base


class XarraySample(Base):
    """
    Sample script that runs xarray functions logged by recipy.

    This class assumes the existence of a data/xarray directory,
    co-located with this file, with the following content:

    * image.tiff
    * soilPropertiesRhineMeuse30min.nc: test netcdf file (taken with permission
      from https://github.com/UU-Hydro/PCR-GLOBWB_input_example, see
      https://www.geosci-model-dev.net/11/2429/2018/gmd-11-2429-2018.html for
      more information about this data)
    * topoPropertiesRhineMeuse30min.nc: test netcdf file (taken with permission
      from https://github.com/UU-Hydro/PCR-GLOBWB_input_example, see
      https://www.geosci-model-dev.net/11/2429/2018/gmd-11-2429-2018.html for
      more information about this data)
    * data_array.nc: netcdf file containing a dataarray (instead of a dataset)
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "xarray")

    def open_dataset(self):
        """
        Use xarray.open_dataset to read netcdf file.
        """
        file_name = os.path.join(self.data_dir,
                                 "soilPropertiesRhineMeuse30min.nc")
        xarray.open_dataset(file_name)

    def open_mfdataset_glob(self):
        """
        Use xarray.open_mfdataset to read multiple netcdf files with a glob
        pattern.
        """
        pattern = os.path.join(self.data_dir, "*PropertiesRhineMeuse30min.nc")
        xarray.open_mfdataset(pattern)

    def open_mfdataset_list(self):
        """
        Use xarray.open_mfdataset to read multiple netcdf files from a list.
        """
        file_names = [os.path.join(self.data_dir, f)
                      for f in ('soilPropertiesRhineMeuse30min.nc',
                                'topoPropertiesRhineMeuse30min.nc')]
        xarray.open_mfdataset(file_names)

    def open_rasterio(self):
        """
        Use xarray.open_rasterio to read image.tiff.
        """
        file_name = os.path.join(self.data_dir, "image.tiff")
        xarray.open_rasterio(file_name)

    def open_dataarray(self):
        """
        Use xarray.open_dataarray to read a netcdf file.
        """
        file_name = os.path.join(self.data_dir, "data_array.nc")
        xarray.open_dataarray(file_name)

    def dataset_to_netcdf(self):
        """
        Use xarray.Dataset.to_netcdf to write a netcdf file.
        """
        data = xarray.DataArray(np.random.randn(2, 3))
        ds = xarray.Dataset({'foo': data, 'bar': ('x', [1, 2]), 'baz': np.pi})
        file_name = os.path.join(self.data_dir, "data.nc")
        ds.to_netcdf(file_name)
        os.remove(file_name)

    def dataarray_to_netcdf(self):
        """
        Use xarray.DataArray.to_netcdf to write a netcdf file.
        """
        data = xarray.DataArray(np.random.randn(2, 3))
        file_name = os.path.join(self.data_dir, "data.nc")
        data.to_netcdf(file_name)
        os.remove(file_name)


if __name__ == "__main__":
    XarraySample().invoke(sys.argv)
