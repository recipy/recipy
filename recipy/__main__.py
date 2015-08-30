# Allow any python script to run under recipy by using ::
#
#   python -m recipy <script>.py <args>

if __name__ == '__main__':
    from sys import argv
    from runpy import run_path
    # The first argument is the full path to this module so remove it
    argv.pop(0)
    # Run the user script
    run_path(argv[0])
