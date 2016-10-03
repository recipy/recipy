#!/usr/bin/env python
import os
import sys
import six
import click

from recipyCommon import config, utils
from recipyCommon.config import read_config_file
from recipyCmd.templating import render_debug_template


class CliConfig(object):
    """Passes configuration between commands."""
    def __init__(self):
        self.debug = False
        self.db = utils.open_or_create_db()

pass_config = click.make_pass_decorator(CliConfig, ensure=True)


class CLI(click.MultiCommand):
    """Implements MultiCommand click class methods to find other
    commands in the cmd_folder. Command files must be in
    format cmd_COMMANDNAME.py"""

    def list_commands(self, ctx):
        cmd = []
        cmd_folder = os.path.dirname(__file__)
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and filename.startswith('cmd_'):
                cmd.append(filename[4:-3])
        cmd.sort()
        return cmd

    def get_command(self, ctx, cmd_name):
        try:
            if sys.version_info[0] == 2:
                cmd_name = cmd_name.encode('ascii', 'replace')
            mod = __import__('recipyCmd.cmd_' + cmd_name, fromlist=['cmd'])
        except ImportError:
            return
        return mod.cmd


@click.command(cls=CLI)
@click.version_option(version='0.1.0')
@click.option('--debug', is_flag=True,
              help='Show debug info while running command.')
@pass_config
def main(config, debug):
    """Frictionless provenance tracking in Python.
    For more info type: recipy COMMAND --help"""
    config.debug = debug
    if config.debug:
        click.echo(debug_info())


def debug_info():
    cnf = read_config_file()
    s = six.StringIO()
    cnf.write(s)
    return render_debug_template(config.get_db_path(), s.getvalue())
