import sys
import imp

import functools
from recipyCommon.config import option_set
from recipyCommon.utils import recursive_find_module

class PatchImporter(object):
    """A class that handles finding modules, importing them
    and calling a `patch` method.

    This class is not designed to be used itself - instead,
    subclasses should be created that implement the `patch` method.
    """
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
        """Module loading method. It imports the module normally,
        and then calls the `patch` method to wrap the functions we need.

        `patch` is implemented by subclasses
        """
        if name != self.modulename:
            raise ImportError("%s can only be used to import a specific module!",
                              self.__class__.__name__)
        if name in sys.modules:
            return sys.modules[name]    # already imported and patched
        
        # Find the module
        file_obj, pathname, desc = recursive_find_module(name, sys.path)

        try:
            mod = imp.load_module(name, file_obj, pathname, desc)
        finally:
            if file_obj:
                file_obj.close()
        
        if option_set('general', 'debug'):
            print("Patching %s" % mod.__name__)

        # Actually do the patching
        mod = self.patch(mod)

        # And put the module in Python's proper namespace
        sys.modules[name] = mod

        return mod

    
    def patch(self, mod):
        return mod
