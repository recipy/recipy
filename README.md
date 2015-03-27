# What is it?


# Installation:
You will need to install the following python packages:
 * `pymongo`
 * `wrapt`

You can install these by running:

    pip install pymongo
    pip install wrapt

If you want to run the example scripts that come with recipy then you'll also need to have `numpy`, `pandas` and `matplotlib` installed.

You'll also need to install MongoDB (`brew install mongodb` if you're running OS X) and run it locally with the command `mongod`.

# Usage
Simply add the following line to the top of your Python script:

    import recipy

Note that this must be the *very top* line of your script, before you import anything else.

Then just run your script as usual, and all of the data will be logged into the MongoDB database. You can use the `recipy-cmd` script to quickly query the database to find out what run of your code produced what output file. So, for example, if you add `import recipy` to the top of 'example_script3.py' and then run:

    python example_script3.py
    
it will produce an output called `ALongTimeAgo.npy`. To find out the details of the run which created this file you can search using

    ./recipy-cmd ALongTimeAgo.npy

and it will display information like the following:

    {u'_id': ObjectId('55156a7bfdfff4038857d6ea'),
    u'author': u'robin',
     u'command': u'example_script3.py',
     u'date': datetime.datetime(2015, 3, 27, 14, 34, 35, 24000),
     u'description': u'',
     u'environment': [u'python3.2', u'PyMongo2.8', u'MAC OS 10.10.02'],
     u'gitcommit': u'6a8b3c06c9b5c66b1bb48ba0dd3928d8ef748f84',
     u'gitrepo': u'https://github.com/recipy/recipy.git',
     u'gituser': u'robintw',
     u'inputs': [u'/Users/robin/code/recipy/data.csv'],
     u'outputs': [u'ALongTimeAgo.npy'],
     u'script': u'example_script3.py'}
    

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
