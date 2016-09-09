from git import Repo, InvalidGitRepositoryError
import hashlib
from recipyCommon.config import option_set


def hash_file(path):
    try:
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        with open(path, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()
    except Exception:
        return None


def get_origin(repo):
    try:
        return repo.remotes.origin.url
    except:
        return None


def add_git_info(run, scriptpath):
    """Add information about the git repository holding the source file to the database"""
    try:
        repo = Repo(scriptpath, search_parent_directories=True)
        run["gitrepo"] = repo.working_dir
        run["gitcommit"] = repo.head.commit.hexsha
        run["gitorigin"] = get_origin(repo)

        if not option_set('ignored metadata', 'diff'):
            whole_diff = ''
            diffs = repo.index.diff(None, create_patch=True)
            for diff in diffs:
                whole_diff += "\n\n\n" + "--- {}\n+++ {}\n".format(
                    diff.a_path, diff.b_path) + diff.diff.decode("utf-8")

            run['diff'] = whole_diff
    except (InvalidGitRepositoryError, ValueError):
        # We can't store git info for some reason, so just skip it
        pass
