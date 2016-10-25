"""
Sample script that runs pandas functions logged by recipy.
"""

# Copyright (c) 2016 University of Edinburgh.

import recipy

import os
import string
import sys
import pandas as pd

from integration_test.packages.base import Base


class PandasSample(Base):
    """
    Sample script that runs pandas functions logged by recipy.

    This class assumes the existence of a data/pandas directory,
    co-located with this file, with the following content:

    * dataframe.csv: comma-separated values
    * dataframe.xls: Pandas-compliant Excel
    * dataframe.hdf: HDF5 file
    * dataframe.pickle: Pickle file. It is assumed this is created under
      Python 2.7 and can be read using both Python 2.7 and 3.4.
    * dataframe.dta: Stata file
    * dataframe.mpack: MsgPack file

    Running this script with argument 'create_sample_data' will create
    these files.

    All functions that save files delete the files after saving,
    to keep the directory clean.
    """

    def __init__(self):
        """
        Constructor. Set data_dir attribute with path to data files needed
        by this class.
        """
        Base.__init__(self)
        self.data_dir = os.path.join(self.current_dir, "data", "pandas")
        print(("Data directory: ", self.data_dir))

    def get_data(self, i, j, offset=0):
        """
        Return dictionary of characters to integers. For example:

        * i=0, j=4, yields {'a': 0, 'b': 1, 'c': 2, 'd': 3}
        * i=0, j=4, offset=2 yields {'a': 2, 'b': 3, 'c': 4, 'd': 5}

        :param i: Index of first character (assuming 'a' is 0 etc).
        :type i: int
        :param j: Index of last character.
        :type j: int
        :param offset: Offset to be added to integer that character maps
        to
        :type offset: int
        :return: dictionary of characters to integers
        :rtype: dict
        """
        return {string.ascii_lowercase[y]: (y + offset)
                for y in range(i, j)}

    def get_series(self, i, j, offset=0):
        """
        Return output from get_data as a pandas Series object.

        :param i: Index of first character (assuming 'a' is 0 etc).
        :type i: int
        :param j: Index of last character.
        :type j: int
        :param offset: Offset to be added to integer that character maps
        to
        :type offset: int
        :return: Series
        :rtype: pandas.Series
        """
        return pd.Series(self.get_data(i, j, offset))

    def get_dataframe(self):
        """
        Return a DataFrame consisting of two Series, each created using
        get_series.

        :return: DataFrame
        :rtype: pandas.DataFrame
        """
        data = {'seriesOne': self.get_series(0, 5),
                'seriesTwo': self.get_series(0, 5, 10)}
        frame = pd.DataFrame(data)
        return frame

    def get_panel(self):
        """
        Return a Panel consisting of two DataFrames, each consisting
        of two Series, each created using get_series.

        :return: Panel
        :rtype: pandas.Panel
        """
        data1 = {'seriesOne': self.get_series(0, 5),
                 'seriesTwo': self.get_series(0, 5, 10)}
        frame1 = pd.DataFrame(data1)
        data2 = {'seriesThree': self.get_series(6, 10),
                 'seriesFour': self.get_series(6, 10, 10)}
        frame2 = pd.DataFrame(data2)
        data = {'frameOne': frame1, 'frameTwo': frame2}
        return pd.Panel(data)

    def read_csv(self):
        """
        Use pandas.read_csv to load dataframe.csv.
        """
        file_name = os.path.join(self.data_dir, "dataframe.csv")
        print(("Loading data:", file_name))
        data = pd.read_csv(file_name)
        print("Data:")
        print((data))

    def read_table(self):
        """
        Use pandas.read_table to load dataframe.csv.
        """
        file_name = os.path.join(self.data_dir, "dataframe.csv")
        print(("Loading data:", file_name))
        data = pd.read_table(file_name)
        print("Data:")
        print((data))

    def read_excel(self):
        """
        Use pandas.read_excel to load dataframe.xls.
        """
        file_name = os.path.join(self.data_dir, "dataframe.xls")
        print(("Loading data:", file_name))
        data = pd.read_excel(file_name)
        print("Data:")
        print((data))

    def read_hdf(self):
        """
        Use pandas.read_hdf to load dataframe.hdf.
        """
        file_name = os.path.join(self.data_dir, "dataframe.hdf")
        print(("Loading data:", file_name))
        data = pd.read_hdf(file_name)
        print("Data:")
        print((data))

    def read_pickle(self):
        """
        Use pandas.read_pickle to load dataframe.pickle.
        """
        file_name = os.path.join(self.data_dir, "dataframe.pickle")
        print(("Loading data:", file_name))
        data = pd.read_pickle(file_name)
        print("Data:")
        print((data))

    def read_stata(self):
        """
        Use pandas.read_stata to load dataframe.dta.
        """
        file_name = os.path.join(self.data_dir, "dataframe.dta")
        print(("Loading data:", file_name))
        data = pd.read_stata(file_name)
        print("Data:")
        print((data))

    def read_msgpack(self):
        """
        Use pandas.read_msgpack to load dataframe.mpack.
        """
        file_name = os.path.join(self.data_dir, "dataframe.mpack")
        print(("Loading data:", file_name))
        data = pd.read_msgpack(file_name)
        print("Data:")
        print((data))

    def panel_to_excel(self):
        """
        Use pandas.Panel.to_excel to save a file out.xls.
        """
        file_name = os.path.join(self.data_dir, "out.xls")
        panel = self.get_panel()
        print(("Saving data:", file_name))
        panel.to_excel(file_name)
        os.remove(file_name)

    def panel_to_hdf(self):
        """
        Use pandas.Panel.to_hdf to save a file out.hdf.
        """
        file_name = os.path.join(self.data_dir, "out.hdf")
        panel = self.get_panel()
        print(("Saving data:", file_name))
        panel.to_hdf(file_name, key="Sample", mode="w")
        os.remove(file_name)

    def panel_to_msgpack(self):
        """
        Use pandas.Panel.to_msgpack to save a file out.mpack.
        """
        file_name = os.path.join(self.data_dir, "out.mpack")
        panel = self.get_panel()
        print(("Saving data:", file_name))
        panel.to_msgpack(file_name)
        os.remove(file_name)

    def panel_to_pickle(self):
        """
        Use pandas.Panel.to_pickle to save a file out.pickle.
        """
        file_name = os.path.join(self.data_dir, "out.pickle")
        panel = self.get_panel()
        print(("Saving data:", file_name))
        panel.to_pickle(file_name)
        os.remove(file_name)

    def dataframe_to_excel(self):
        """
        Use pandas.DataFrame.to_excel to save a file out.xls.
        """
        file_name = os.path.join(self.data_dir, "out.xls")
        dataframe = self.get_dataframe()
        print(("Saving data:", file_name))
        dataframe.to_excel(file_name, sheet_name="SampleSheet")
        os.remove(file_name)

    def dataframe_to_hdf(self):
        """
        Use pandas.DataFrame.to_hdf to save a file out.hdf.
        """
        file_name = os.path.join(self.data_dir, "out.hdf")
        dataframe = self.get_dataframe()
        print(("Saving data:", file_name))
        dataframe.to_hdf(file_name, key="Sample", mode="w")
        os.remove(file_name)

    def dataframe_to_msgpack(self):
        """
        Use pandas.DataFrame.to_msgpack to save a file out.mpack.
        """
        file_name = os.path.join(self.data_dir, "out.mpack")
        dataframe = self.get_dataframe()
        print(("Saving data:", file_name))
        dataframe.to_msgpack(file_name)
        os.remove(file_name)

    def dataframe_to_pickle(self):
        """
        Use pandas.DataFrame.to_pickle to save a file out.pickle.
        """
        file_name = os.path.join(self.data_dir, "out.pickle")
        dataframe = self.get_dataframe()
        print(("Saving data:", file_name))
        dataframe.to_pickle(file_name)
        os.remove(file_name)

    def dataframe_to_csv(self):
        """
        Use pandas.DataFrame.to_csv to save a file out.csv.
        """
        file_name = os.path.join(self.data_dir, "out.csv")
        dataframe = self.get_dataframe()
        print(("Saving data:", file_name))
        dataframe.to_csv(file_name)
        os.remove(file_name)

    def dataframe_to_stata(self):
        """
        Use pandas.DataFrame.to_stata to save a file out.dta.
        """
        file_name = os.path.join(self.data_dir, "out.dta")
        dataframe = self.get_dataframe()
        print(("Saving data:", file_name))
        dataframe.to_stata(file_name)
        os.remove(file_name)

    def series_to_hdf(self):
        """
        Use pandas.Series.to_hdf to save a file out.hdf.
        """
        file_name = os.path.join(self.data_dir, "out.hdf")
        series = self.get_series(0, 4)
        print(("Saving data:", file_name))
        series.to_hdf(file_name, key="Sample", mode="w")
        os.remove(file_name)

    def series_to_msgpack(self):
        """
        Use pandas.Series.to_msgpack to save a file out.mpack.
        """
        file_name = os.path.join(self.data_dir, "out.mpack")
        series = self.get_series(0, 4)
        print(("Saving data:", file_name))
        series.to_msgpack(file_name)
        os.remove(file_name)

    def series_to_pickle(self):
        """
        Use pandas.Series.to_pickle to save a file out.pickle.
        """
        file_name = os.path.join(self.data_dir, "out.pickle")
        series = self.get_series(0, 4)
        print(("Saving data:", file_name))
        series.to_pickle(file_name)
        os.remove(file_name)

    def series_to_csv(self):
        """
        Use pandas.Series.to_csv to save a file out.csv.
        """
        file_name = os.path.join(self.data_dir, "out.csv")
        series = self.get_series(0, 4)
        print(("Saving data:", file_name))
        series.to_csv(file_name)
        os.remove(file_name)

    def create_sample_data(self):
        """
        Create sample data files. The files created are:

        * dataframe.csv: comma-separated values
        * dataframe.xls: Pandas-compliant Excel
        * dataframe.hdf: HDF5 file
        * dataframe.pickle: Pickle file
        * dataframe.dta: Stata file
        * dataframe.mpack: MsgPack file
        """
        dataframe = self.get_dataframe()
        file_name = os.path.join(self.data_dir, "dataframe.xls")
        dataframe.to_excel(file_name, sheet_name="SampleSheet")
        file_name = os.path.join(self.data_dir, "dataframe.hdf")
        dataframe.to_hdf(file_name, key="Sample", mode="w")
        file_name = os.path.join(self.data_dir, "dataframe.mpack")
        dataframe.to_msgpack(file_name)
        file_name = os.path.join(self.data_dir, "dataframe.pickle")
        dataframe.to_pickle(file_name)
        file_name = os.path.join(self.data_dir, "dataframe.csv")
        dataframe.to_csv(file_name)
        file_name = os.path.join(self.data_dir, "dataframe.dta")
        dataframe.to_stata(file_name)


if __name__ == "__main__":
    pandas_sample = PandasSample()
    pandas_sample.invoke(sys.argv)
