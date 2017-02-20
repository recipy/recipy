from recipyCommon.config import find_editor

import unittest
import mock


class TestConfig(unittest.TestCase):
    def test_find_editor_windows(self):
        with mock.patch('sys.platform', 'win32'):
            with mock.patch('recipyCommon.config._try_editors', return_value='notepad'):
                editor = find_editor()

        self.assertEquals(editor, 'notepad')

    def test_find_editor_mac(self):
        with mock.patch('sys.platform', 'darwin'):
            with mock.patch('recipyCommon.config._try_editors', return_value='open -t'):
                editor = find_editor()

        self.assertEquals(editor, 'open -t')

    def test_find_editor_linux(self):
        with mock.patch('sys.platform', 'linux'):
            with mock.patch('recipyCommon.config._try_editors', return_value='vi'):
                editor = find_editor()

        self.assertEquals(editor, 'vi')
