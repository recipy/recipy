from recipyCmd.recipycmd import main as cli


def test_latest_shows_latest_run(runner, config):
    result = runner.invoke(cli, ['latest'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'Run ID: latest_run' in result.output


def test_latest_shows_diff_on_run(runner, config):
    result = runner.invoke(cli, ['latest', '--diff'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'diff of latest run' in result.output


def test_latest_shows_run_as_json(runner, config):
    result = runner.invoke(cli, ['latest', '--json'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert '{\n  "date": "{TinyDate}:2016-08-16T17:20:08"' in result.output


def test_latest_prints_message_on_empty_db(runner, config_empty_db):
    result = runner.invoke(cli, ['latest'], obj=config_empty_db)
    assert not result.exception
    assert result.exit_code == 0
    assert 'Database is empty.' in result.output


def test_latest_prints_empty_json_on_empty_db(runner, config_empty_db):
    result = runner.invoke(cli, ['latest', '--json'], obj=config_empty_db)
    assert not result.exception
    assert result.exit_code == 0
    assert '[]' in result.output
