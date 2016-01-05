from git import Git, Repo, GitCommandError, InvalidGitRepositoryError

from recipyCommon.config import option_set


def git_hash_object(path):
    # Evaluate git-hash-object on path (even for files outside of repo)
    try:
        return Git().hash_object(path)
    except GitCommandError:  # e.g. file does not exist
        return None

def add_git_info(run, scriptpath):
    try:
        repo = Repo(scriptpath, search_parent_directories=True)
        run["githash"] = git_hash_object(scriptpath)
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
