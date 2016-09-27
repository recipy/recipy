import pytest
from click.testing import CliRunner
from recipyCmd import recipycmd as cli


@pytest.fixture
def runner():
    return CliRunner()


def test_main_with_no_arguments_shows_help(runner):
    result = runner.invoke(cli.main)
    assert not result.exception
    assert result.exit_code == 0


def test_main_correctly_passes_config(runner):
    result = runner.invoke(cli.main,
                           ['--debug', 'annotate'])
    assert not result.exception
    assert result.exit_code == 0
    assert 'Debug info...' in result.output
