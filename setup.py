# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='recipy',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.2.1',

    description='A frictionless provenance framework for Python',
    long_description="""A frictionless provenance framework for Python.

Please see https://github.com/recipy/recipy for further information.
""",

    # The project's main homepage.
    url='https://github.com/recipy/recipy',

    # Author details
    author='Robin Wilson, Raquel Alegre, Janneke van der Zwaan',
    author_email='robin@rtwilson.com',

    # Choose your license
    license='Apache',

    include_package_data=True,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='development, science, reproducibility, provenance',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['wrapt', 'tinydb', 'jinja2', 'docopt', 'GitPython', 'Flask',
                      'Flask-Script', 'flask_bootstrap', 'flask-wtf', 'python-dateutil',
                      'six'],

    entry_points={
        'console_scripts': [
            'recipy=recipyCmd.recipycmd:main',
        ]
    }

    #scripts=['recipy-cmd']
)