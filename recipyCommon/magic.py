from IPython.core.magic import Magics, magics_class, line_magic
import warnings

import json
import os
import re
import ipykernel
import requests
import tempfile
import base64

from requests.compat import urljoin

from notebook.notebookapp import list_running_servers

from recipy.log import log_output
from recipyCommon.config import set_notebook_name


embedded_image_types = ("<class 'IPython.core.display.Image'>")
formats = ('image/png', 'image/jpeg')


@magics_class
class RecipyMagic(Magics):
    def __init__(self, shell):
        super(RecipyMagic, self).__init__(shell)
        self.recipyModule = None
        self.run_in_progress = False
        self.ran_recipyOn = False

        set_notebook_name(self.get_notebook_name())

        import recipy
        self.recipyModule = recipy

    def get_notebook_name(self):
        """
        Return the full path of the jupyter notebook.

        Taken from https://github.com/jupyter/notebook/issues/1000
        """
        try:
            connection_file = ipykernel.connect.get_connection_file()
            kernel_id = re.search('kernel-(.*).json', connection_file).group(1)
            servers = list_running_servers()
            for ss in servers:
                response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                        params={'token': ss.get('token', '')})
                for nn in json.loads(response.text):
                    if nn['kernel']['id'] == kernel_id:
                        relative_path = nn['notebook']['path']
                        return os.path.join(ss['notebook_dir'], relative_path)
        except RuntimeError:
            # We are probably running tests
            return 'test_notebook.ipynb'
        return None

    @line_magic
    def recipyOn(self, line):
        "my line magic"
        # print("Full access to the main IPython object:", self.shell)
        # print("Variables in the user namespace:", list(self.shell.user_ns.keys()))

        if self.run_in_progress:
            msg = 'Run in progress. Please run %recipyOff to finish the ' \
                  'current run before starting a new one.'
            warnings.warn(msg, RuntimeWarning)
            return

        set_notebook_name(self.get_notebook_name())

        # No need to do log_init() the first time recipyOn is run after loading
        # the extension (and importing recipy), because it is done when recipy
        # is imported.
        if self.ran_recipyOn:
            self.recipyModule.log_init()
        self.ran_recipyOn = True
        self.run_in_progress = True
        return None

    @line_magic
    def recipyOff(self, line):
        "my line magic"
        # print("Full access to the main IPython object:", self.shell)
        # print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        if self.run_in_progress:
            # Find embedded images
            temp_files = []
            hm = self.shell.history_manager
            fmt = self.shell.display_formatter.format
            for session, lineno, inp in hm.get_range(session=0):
                try:
                    obj = self.shell.user_ns['Out'][lineno]
                    if str(obj.__class__) in embedded_image_types:
                        # Save to temporary file
                        fd, path = tempfile.mkstemp(prefix='embedded_image_')
                        temp_files.append(path)

                        formatted = fmt(obj, include=formats)

                        for typ, data in formatted[0].items():
                            # TODO: fix case when formatted[0] contains more
                            # than one entry
                            with open(path, 'wb') as f:
                                f.write(base64.b64decode(data))

                        # Log output
                        # TODO: get the correct module
                        # TODO: only log when file hashes are added, because
                        # otherwise the only information that is logged is the
                        # fact that there are embedded images
                        log_output(path, 'recipy')

                except KeyError:
                    pass

            self.recipyModule.log_flush()
            self.run_in_progress = False

            # Remove temporary file(s)
            for fname in temp_files:
                os.remove(fname)
        else:
            warnings.warn('Please run %recipyOn before running %recipyOff.',
                          RuntimeWarning)
        return None


def load_ipython_extension(ipython):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    ipython.register_magics(RecipyMagic)


def unload_ipython_extension(ipython):
    # If you want your extension to be unloadable, put that logic here.
    pass
