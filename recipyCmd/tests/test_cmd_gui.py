import sys
import pytest
import click
from recipyCmd.recipycmd import main as cli


def fake_gui(_, debug='', port=''):
    click.echo('Gui started on {}'.format(port))
    click.echo('Gui started in debug={}'.format(debug))


@pytest.mark.skipif(sys.version_info < (3,3), reason='Needs fix which method to mock on timer in Python 2.7')
def test_gui_tries_to_launch_browser(runner, config, monkeypatch):
    """This only checks whether the command has been passed
    properly to RecipyGui mocks starting Flask and browser"""
    monkeypatch.setattr('flask.Flask.run', fake_gui)
    monkeypatch.setattr('threading.Timer.start', lambda x: click.echo('Browser started'))
    result = runner.invoke(cli, ['gui'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'Gui started on' in result.output
    assert 'Gui started in debug=False' in result.output
    assert 'Browser started' in result.output


@pytest.mark.skipif(sys.version_info < (3,3), reason='Needs fix which method to mock on timer in Python 2.7')
def test_gui_will_not_launch_browser(runner, config, monkeypatch):
    """This only checks whether the command has been passed
    properly to RecipyGui mocks starting Flask"""
    monkeypatch.setattr('flask.Flask.run', fake_gui)
    monkeypatch.setattr('threading.Timer.start', lambda x: click.echo('Browser started'))
    result = runner.invoke(cli, ['gui', '--no-browser'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'Gui started on' in result.output
    assert 'Gui started in debug=False' in result.output
    assert 'Browser started' not in result.output
