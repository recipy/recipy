from .PatchSimple import PatchSimple

from recipyCommon.config import option_set
from recipyCommon.utils import patch_function


class PatchFileOpenLike(PatchSimple):
    """Object that patches a function and either logs it as input or output
    based on an argument/implemented function.

    Should be subclassed.
    """
    def patch(self, mod):
        for f in self.functions:
            if option_set('general', 'debug'):
                print('Patching input/output function: {}'.format(f))
            patch_function(mod, f, self.wrapper)

        return mod
