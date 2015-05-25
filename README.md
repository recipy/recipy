# What is it and who cares?
Have you ever run some Python scripts to produce some outputs - such as graphs or output CSV files - and then forgotten exactly how you created them? For example, you have a lovely graph in plot.pdf, but you don't know how you created it, and therefore can't use it in a journal paper.

Recipy (from *recipe* and *python*) will come to your rescue! With almost no extra work (literally the addition of a single line of code to your Python script), it will monitor the inputs and outputs of the script and store this information in a database so you can easily query it.

It's great!

# Installation:
You will need to install the following python packages:
 * `pymongo`
 * `wrapt`

You can install these by running:

    pip install pymongo
    pip install wrapt

If you want to run the example scripts that come with recipy then you'll also need to have `numpy`, `pandas` and `matplotlib` installed.

You'll also need to install MongoDB (`brew install mongodb` if you're running OS X) and run it locally with the command `mongod`.

You may want to install [recipy-gui](https://github.com/recipy/recipy-gui) for a nice way to view the data.

# Usage
Simply add the following line to the top of your Python script:

    import recipy

Note that this must be the *very top* line of your script, before you import anything else.

Then just run your script as usual, and all of the data will be logged into the MongoDB database. You can use the `recipy-cmd` script to quickly query the database to find out what run of your code produced what output file. So, for example, if you add `import recipy` to the top of 'example_script3.py' and then run:

    python example_script.py
    
it will produce an output called `newplot.pdf`. To find out the details of the run which created this file you can search using

    ./recipy-cmd newplot.pdf

and it will display information like the following:

    Created by robin on 2015-05-25 19:00:15.631000
	Ran /Users/robin/code/recipy/example_script.py using /usr/local/opt/python/bin/python2.7
	Git: commit 91a245e5ea82f33ae58380629b6586883cca3ac4, in repo /Users/robin/code/recipy, with origin git@github.com:recipy/recipy.git
	Environment: Darwin-14.3.0-x86_64-i386-64bit, python 2.7.9 (default, Feb 10 2015, 03:28:08)
	Inputs:
	  /Users/robin/code/recipy/data.csv

	Outputs:
	  /Users/robin/code/recipy/newplot.pdf

	** Previous runs creating this output have been found. Run with --all to show. **
    
Run `./recipy-cmd --help` to see the other options: you can view diffs, all runs that created a file with that name, and more:

	recipy - a frictionless provenance tool for Python

	Usage:
	  recipy-cmd [options] <outputfile>
	  recipy-cmd (-h | --help)
	  recipy-cmd --version

	Options:
	  -h --help     Show this screen
	  --version     Show version
	  -a --all      Show all results (otherwise just latest result given)
	  -f --fuzzy    Use fuzzy searching on filename
	  -r --regex    Use regex searching on filename
	  -v --verbose  Be verbose
	  -d --diff     Show diff
	  --debug       Turn on debugging mode

# How it works
When you import recipy it adds a number of classes to `sys.meta_path`. These are then used by Python as part of the importing procedure for modules. The classes that we add are classes derived from `PatchImporter`, often using the easier interface provided by `PatchSimple`, which allow us to wrap functions that do input/output in a function that calls recipy first to log the information.

Generally, most of the complexity is hidden away in `PatchImporter` and `PatchSimple` (plus `utils.py`), so the actual code to wrap a module, such as `numpy` is fairly simple:

	# Inherit from PatchSimple
	class PatchNumpy(PatchSimple):
		# Specify the full name of the module
	    modulename = 'numpy'

	    # List functions that are involved in input/output
	    # these can be anything that can go after "modulename."
	    # so they could be something like "pyplot.savefig" for example
	    input_functions = ['genfromtxt', 'loadtxt', 'load', 'fromfile']
	    output_functions = ['save', 'savez', 'savez_compressed', 'savetxt']

	    # Define the functions that will be used to wrap the input/output
	    # functions.
	    # In this case we are calling the log_input function to log it to the DB
	    # and we are giving it the 0th argument from the function (because all of
	    # the functions above take the filename as the 0th argument), and telling
	    # it that it came from numpy.
	    input_wrapper = create_wrapper(log_input, 0, 'numpy')
	    output_wrapper = create_wrapper(log_output, 0, 'numpy')
