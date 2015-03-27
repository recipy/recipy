import sys
import imp
import wrapt

 
import functools
from datetime import timedelta 

@wrapt.decorator
def log(wrapped, instance, args, kwargs):
    print "Logging"
    print args
    return wrapped(*args, **kwargs)
 
class PandasImporter(object):
    """Finder and loader class for the pytz module.
    
    This is the main part of import hook that
    will be executed specifically for pytz when it's
    about to be imported.
    When it happens, we inject our generic timezones
    into all relevant places inside pytz so that they
    can be freely used alongside others.
    """
    def find_module(self, fullname, path=None):
        """Module finding method. It tells Python to use our hook
        only for the pytz package.
        """
        if fullname == 'pandas':
            self.path = path
            return self
        return None
    
    def load_module(self, name):
        """Module loading method. It imports pytz normally
        and then enhances it with our generic timezones.
        """
        if name != 'pandas':
            raise ImportError("%s can only be used to import pandas!",
                              self.__class__.__name__)
        if name in sys.modules:
            return sys.modules[name]    # already imported
        
        file_obj, pathname, desc = imp.find_module(name, self.path)
        try:
            pandas = imp.load_module(name, file_obj, pathname, desc)
        finally:
            if file_obj:
                file_obj.close()
        
        print "Enhancing!"
        pandas = self.__enhance_pandas(pandas)
        sys.modules[name] = pandas
        return pandas

    
    def __enhance_pandas(self, pandas):
        pandas._read_csv = pandas.read_csv
        pandas.read_csv = log(pandas.read_csv)
        
        return pandas
    
    def __get_generic_timezones(self):
        """Returns dictionary mapping names of our generic
        GMT timezones to their offsets from UTC in minutes.
        """
        span = range(-12, 14 + 1)
        span.remove(0) # pytz alrady has GMT
        return dict(('GMT%(sign)s%(offset)s' % {
                        'sign': '+' if i > 0 else '-',
                        'offset': abs(i),
                     }, timedelta(hours=i).total_seconds() // 60)
                     for i in span)
        
sys.meta_path = [PandasImporter()]