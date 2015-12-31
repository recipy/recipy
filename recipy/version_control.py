from git import Repo, InvalidGitRepositoryError

from recipyCommon.config import option_set


def add_git_info(run, scriptpath):
    try:
        repo = Repo(scriptpath, search_parent_directories=True)
        run["gitrepo"] = repo.working_dir
        run["gitcommit"] =  repo.head.commit.hexsha
        try:
            run["gitorigin"] = repo.remotes.origin.url
        except:
            run["gitorigin"] = None

        if not option_set('ignored metadata', 'diff'):
            whole_diff = ''
            diffs = repo.index.diff(None, create_patch=True)
            for diff in diffs:
                whole_diff += "\n\n\n" + diff.diff.decode("utf-8")

            run['diff'] = whole_diff
    except (InvalidGitRepositoryError, ValueError):
        # We can't store git info for some reason, so just skip it
        pass
