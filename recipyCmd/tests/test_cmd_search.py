from recipyCmd.recipycmd import main as cli


def test_search_requires_file(runner, config):
    result = runner.invoke(cli, ['search'], obj=config)
    assert result.exception
    assert result.exit_code == 2
    assert 'Error: Missing argument "file"' in result.output.strip()
