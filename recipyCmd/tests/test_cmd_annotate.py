from tinydb import TinyDB, where
from recipyCmd.recipycmd import main as cli


def test_annotate_adds_note_to_latest_run(runner, config, monkeypatch, path_to_db):
    monkeypatch.setattr('recipyCmd.cmd_annotate.get_message', lambda x: 'New Message')
    result = runner.invoke(cli, ['annotate'], obj=config)
    with TinyDB(path_to_db) as db:
        run = db.search(where('unique_id') == 'latest_run')[0]
        assert 'New Message' in run['notes']
    assert not result.exception
    assert result.exit_code == 0
    assert 'Note successfully added to run' in result.output


def test_annotate_adds_note_to_run_with_a_note(runner, config, monkeypatch, path_to_db):
    monkeypatch.setattr('recipyCmd.cmd_annotate.get_message', lambda x: 'Another Message')
    result = runner.invoke(cli, ['annotate', '--id=765a'], obj=config)
    with TinyDB(path_to_db) as db:
        run = db.search(where('unique_id') == '765a35e7')[0]
        assert 'Another Message' in run['notes']
    assert not result.exception
    assert result.exit_code == 0
    assert 'Note successfully added to run' in result.output


def test_annotate_cannot_find_unique_run(runner, config):
    result = runner.invoke(cli, ['annotate', '--id=665'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'Found more then one run starting with id 665. Please expand id.' in\
           result.output


def test_annotate_cannot_find_a_run(runner, config):
    result = runner.invoke(cli, ['annotate', '--id=doesnotexist'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'Could not find run starting with id doesnotexist' in result.output


def test_annotate_does_not_add_note_if_note_empty(runner, config, monkeypatch, path_to_db):
    monkeypatch.setattr('recipyCmd.cmd_annotate.get_message', lambda x: '')
    result = runner.invoke(cli, ['annotate', '--id=765a35e7'], obj=config)
    with TinyDB(path_to_db) as db:
        run = db.search(where('unique_id') == '765a35e7')[0]
        assert 'original note' in run['notes']
    assert not result.exception
    assert result.exit_code == 0
    assert 'No notes added to run 765a35e7' in result.output


def test_main_prints_additional_debug_information(runner, config, monkeypatch):
    monkeypatch.setattr('recipyCmd.cmd_annotate.get_message', lambda x: '')
    result = runner.invoke(cli, ['--debug', 'annotate'], obj=config)
    assert not result.exception
    assert result.exit_code == 0
    assert 'Full config file (as interpreted):' in result.output