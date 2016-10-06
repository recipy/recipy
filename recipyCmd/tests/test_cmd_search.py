from recipyCmd.recipycmd import main as cli


def test_search_requires_file(runner, config):
    result = runner.invoke(cli, ['search'], obj=config)
    assert result.exception
    assert result.exit_code == 2
    assert 'Error: Missing argument "file"' in result.output.strip()


def test_search_does_not_find_file(runner, config):
    result = runner.invoke(cli, ['search', 'fake_file.txt'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'No runs found.' in result.output


def test_search_json_does_not_find_file(runner, config):
    result = runner.invoke(cli, ['search', '--json', 'fake_file.txt'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'No runs found.' not in result.output
    assert '[]' in result.output


def test_search_fuzzy_finds_latest_run_with_file(runner, config):
    result = runner.invoke(cli, ['search', '--fuzzy', 'plot'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'Older runs found.' in result.output
    assert 'Run ID: latest_run' in result.output
    assert 'early_plot.jpg' in result.output


def test_search_fuzzy_allruns_finds_multiple_runs_with_file(runner, config):
    result = runner.invoke(cli, ['search', '-af', 'plot'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'Older runs found.' not in result.output
    assert 'Run ID: latest_run' in result.output
    assert '665a35e7' in result.output
    assert 'early_plot.jpg' in result.output


def test_search_fuzzy_diff_finds_latest_run_with_file(runner, config):
    result = runner.invoke(cli, ['search', '-fd', 'plot'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'Run ID: latest_run' in result.output
    assert 'diff of latest run' in result.output


def test_search_fuzzy_inputs_finds_latest_run_with_file_in_inputs(runner, config):
    result = runner.invoke(cli, ['search', '-fi', 'input_file'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'Run ID: latest_run' in result.output


def test_search_fuzzy_outputs_does_not_find_existing_file_in_inputs(runner, config):
    result = runner.invoke(cli, ['search', '-fo', 'input_file'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'No runs found.' in result.output
