from recipyCmd import recipycmd as cli


def test_main_with_no_arguments_shows_help(runner):
    result = runner.invoke(cli.main)
    assert not result.exception
    assert result.exit_code == 0
    assert '--version  Show the version and exit.' in result.output
