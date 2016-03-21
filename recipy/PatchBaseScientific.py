import sys
from .PatchImporter import PatchImporter
from .PatchSimple import PatchSimple
import wrapt

from .log import log_input, log_output
from recipyCommon.utils import create_wrapper, multiple_insert

class PatchPandas(PatchSimple):
    modulename = 'pandas'
    input_functions = ['read_csv', 'read_table', 'read_excel', 'read_hdf', 'read_pickle',
        'read_stata', 'read_msgpack']

    output_functions = ['DataFrame.to_csv', 'DataFrame.to_excel', 'DataFrame.to_hdf',
        'DataFrame.to_msgpack', 'DataFrame.to_stata', 'DataFrame.to_pickle']

    output_functions += ['Panel.to_excel', 'Panel.to_hdf',
        'Panel.to_msgpack', 'Panel.to_pickle']

    output_functions += ['Series.to_csv', 'Series.to_hdf',
        'Series.to_msgpack', 'Series.to_pickle']

    input_wrapper = create_wrapper(log_input, 0, 'pandas')
    output_wrapper = create_wrapper(log_output, 0, 'pandas')

class PatchMPL(PatchSimple):
    modulename = 'matplotlib.pyplot'

    input_functions = []
    output_functions = ['savefig']

    input_wrapper = create_wrapper(log_input, 0, 'matplotlib')
    output_wrapper = create_wrapper(log_output, 0, 'matplotlib')

class PatchNumpy(PatchSimple):
    modulename = 'numpy'

    # The `load` function is *deliberately* not included here
    # as it calls fromfile internally, and then we get two duplicate
    # entries recorded in the log
    input_functions = ['genfromtxt', 'loadtxt', 'fromfile']
    output_functions = ['save', 'savez', 'savez_compressed', 'savetxt']

    input_wrapper = create_wrapper(log_input, 0, 'numpy')
    output_wrapper = create_wrapper(log_output, 0, 'numpy')

class PatchLXML(PatchSimple):
    modulename = 'lxml.etree'

    input_functions = ['parse', 'iterparse']
    output_functions = []

    input_wrapper = create_wrapper(log_input, 0, 'lxml')
    output_wrapper = create_wrapper(log_output, 0, 'lxml')

class PatchBS4(PatchSimple):
    modulename = 'bs4'

    input_functions = ['BeautifulSoup']
    output_functions = []

    input_wrapper = create_wrapper(log_input, 0, 'bs4')
    output_wrapper = create_wrapper(log_output, 0, 'bs4')


class PatchCodecs(PatchSimple):
    modulename = 'codecs'

    input_functions = ['open']
    output_functions = []

    input_wrapper = create_wrapper(log_input, 0, 'codecs')
    output_wrapper = create_wrapper(log_output, 0, 'codecs')


multiple_insert(sys.meta_path, [PatchNumpy(), PatchPandas(), PatchMPL(),
                PatchBS4(), PatchLXML(), PatchCodecs()])
