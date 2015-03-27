

# Installation:
You will need to install the following python packages:
 * `pymongo`
 * `wrapt`

You can install these by running:

    pip install pymongo
    pip install wrapt

If you want to run the example scripts that come with recipy then you'll also need to have `numpy`, `pandas` and `matplotlib` installed.


# Usage
Simply add the following line to the top of your Python script:

    import recipy

Note that this must be the *very top* line of your script, before you import anything else.

Then just run your script as usual, and all of the data will be logged into a MongoDB database.

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