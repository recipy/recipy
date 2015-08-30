# Allow any python script to run under recipy by using ::
#
#   python -m recipy SCRIPT [ARGS ...]
from __future__ import print_function

if __name__ == '__main__':
    from sys import argv, exit, stderr
    from runpy import run_path
    # The first argument is the full path to this module so remove it
    argv.pop(0)
    if argv:
        # Run the user script
        run_path(argv[0])
    else:
        print("Usage: python -m recipy SCRIPT [ARGS ...]", file=stderr)
        exit(1)
