from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)

# The class MUST call this class decorator at creation time
@magics_class
class RecipyMagic(Magics):
    def __init__(self, shell):
        super(RecipyMagic, self).__init__(shell)
        self.recipyModule = None

    @line_magic
    def recipyOn(self, line):
        "my line magic"
        # print("Full access to the main IPython object:", self.shell)
        # print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        print("[RecipyMagic] this is when recipy should bet imported, not before...")
        import recipy
        self.recipyModule = recipy
        return None

    @line_magic
    def recipyOff(self, line):
        "my line magic"
        # print("Full access to the main IPython object:", self.shell)
        # print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        self.recipyModule.log_flush()
        return None

def load_ipython_extension(ipython):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    ipython.register_magics(RecipyMagic)

def unload_ipython_extension(ipython):
    # If you want your extension to be unloadable, put that logic here.
    pass
