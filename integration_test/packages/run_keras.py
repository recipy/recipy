"""
Sample script that runs sklearn functions logged by recipy.
"""

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import recipy

import os
import sys
import numpy as np
import keras
import imageio

from integration_test.packages.base import Base


class KerasSample(Base):
    """
    Sample script that runs keras functions logged by recipy.

    This class assumes the existence of a data/keras directory,
    co-located with this file, with the following content:

    * mnist01.jpg
    * mnist02.jpg
    * mnist03.jpg
    * mnist04.jpg
    * mnist05.jpg
    * mnist06.jpg
    * mnist07.jpg
    * mnist08.jpg
    * mnist09.jpg
    * mnist10.jpg
    * mnist.jbl (use X_train, y_train = joblib.load('mnist.jbl'))
    * Model.hdf5


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
        self.data_dir = os.path.join(self.current_dir, "data", "keras")

    def load_svmlight_file(self):
        """
        Use sklearn.datasets.load_svmlight_file to load data.svmlight.
        """
        file_name = os.path.join(self.data_dir, "data.svmlight")
        datasets.load_svmlight_file(file_name)

    def dump_svmlight_file(self):
        """
        Use sklearn.datasets.dump_svmlight_file to save out.svmlight.
        """
        x = np.array([list(range(0, 5)), list(range(5, 10))])
        y = np.array([10, 20])
        file_name = os.path.join(self.data_dir, "out.svmlight")
        datasets.dump_svmlight_file(x, y, file_name,
                                    comment="Sample svmlight file")
        os.remove(file_name)

    def create_sample_data(self):
        """
        Create sample data files. The files created are:

            * mnist01.jpg
            * mnist02.jpg
            * mnist03.jpg
            * mnist04.jpg
            * mnist05.jpg
            * mnist06.jpg
            * mnist07.jpg
            * mnist08.jpg
            * mnist09.jpg
            * mnist10.jpg
            * mnist.jbl (use X_train, y_train = joblib.load('mnist.jbl'))
        """
        (X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

        X_train = X_train[:10, :, :]
        y_train = y_train[:10]

        # Create a list of class folders to create
        classes = np.unique(y_train)

        for cla in classes:
            # Check that the folder exists
            if not os.path.exists(os.path.join(self.data_dir, 'class{}')):
                os.mkdir(os.path.join(self.data_dir, 'class{}'.format(cla)))
        
        for i, (x, y) in enumerate(zip(X_train, y_train)):
            img_name = 'mnist{:0>2d}.jpg'.format(i+1)
            fol = os.path.join(self.data_dir, 'class{}'.format(cla))
            imageio.imwrite(os.path.join(fol, img_name))



        file_name = os.path.join(self.data_dir, "data.svmlight")
        datasets.dump_svmlight_file(x, y, file_name,
                                    comment="Sample svmlight file")


if __name__ == "__main__":
    KerasSample().invoke(sys.argv)
