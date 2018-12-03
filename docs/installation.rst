###################
Installation
###################

The easiest way to install is by simply running:

.. code-block:: sh

    pip install recipy

Alternatively, you can clone this repository and run:

.. code-block:: sh

	python setup.py install

If you want to install the dependencies manually (they should be installed
automatically if you're following the instructions above) then run:

.. code-block:: sh

	pip install -r requirements.txt

You can upgrade from a previous release by running:

.. code-block:: sh

	pip install -U recipy

To find out what has changed since the last release, see the
`changelog <https://github.com/recipy/recipy/blob/master/CHANGELOG.md>`_

**Note:** Previous (unreleased) versions of recipy required MongoDB to be
installed and set up manually. This is no longer required, as a pure Python
database (TinyDB) is used instead. Also, the GUI is now integrated fully into
recipy and does not require installing separately.
