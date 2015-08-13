import sys
import imp

import functools
from .utils import *

CONFIG = open_config_file()


class PatchImporter(object):
    modulename = ''

    def find_module(self, fullname, path=None):
        """Module finding method. It tells Python to use our hook
        only for the package we want.
        """
        #print("Find module: %s" % fullname)
        if fullname == self.modulename:
            self.path = path
            return self
        return None
    
    def load_module(self, name):
        """Module loading method. It imports pytz normally
        and then enhances it with our generic timezones.
        """
        #print("Loading module: %s" % name)
        if name != self.modulename:
            raise ImportError("%s can only be used to import pandas!",
                              self.__class__.__name__)
        if name in sys.modules:
            return sys.modules[name]    # already imported
        
        file_obj, pathname, desc = recursive_find_module(name, sys.path)

        #file_obj, pathname, desc = imp.find_module(name, self.path)
        try:
            mod = imp.load_module(name, file_obj, pathname, desc)
        finally:
            if file_obj:
                file_obj.close()
        
        if option(CONFIG, 'general', 'debug'):
            print("Patching %s" % mod.__name__)
        mod = self.patch(mod)
        sys.modules[name] = mod
        return mod

    
    def patch(self, mod):
        return mod



#sys.meta_path = [PatchImporter()]