import pytest
import sys

from IPython.utils.io import capture_output

# For some reason numpy is already in sys.modules of the interactive shell
# fixture. This means numpy won't be patched, and therefore, can't be used for
# testing the magic. In an actual notebook, numpy can be patched.


def test_recipy_imported_during_loading_of_extension(notebook):
    assert 'recipy' in sys.modules


def test_no_runid_after_recipyon_immediately_after_loading_extension(notebook):
    with capture_output() as output:
        notebook.run_line_magic(magic_name='recipyOn', line='')
    assert 'recipy run inserted, with ID' not in output.stdout

    notebook.run_line_magic(magic_name='recipyOff', line='')

    with capture_output() as output:
        notebook.run_line_magic(magic_name='recipyOn', line='')
    assert 'recipy run inserted, with ID' in output.stdout

    notebook.run_line_magic(magic_name='recipyOff', line='')


def test_run_recipyon_twice_without_running_recipyoff(notebook):
    notebook.run_line_magic(magic_name='recipyOn', line='')
    with capture_output() as output:
        with pytest.warns(RuntimeWarning):
            notebook.run_line_magic(magic_name='recipyOn', line='')
    assert 'recipy run inserted, with ID' not in output.stdout


def test_magic_recipyOff_without_recipyOn(notebook):
    with pytest.warns(RuntimeWarning):
        notebook.run_line_magic(magic_name='recipyOff', line='')
