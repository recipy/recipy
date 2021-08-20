from git import Repo, InvalidGitRepositoryError
import svn.local
import subprocess
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


def get_remotes(repo):
    try:
        names = [x.name for x in repo.remotes]
        urls = [x.url for x in repo.remotes]
        
        return zip(names, urls)
    except:
        return None


def add_git_info(run, scriptpath):
    """Add information about the git repository holding the source file to the database"""
    try:
        repo = Repo(scriptpath, search_parent_directories=True)
        run["gitrepo"] = repo.working_dir
        run["gitcommit"] = repo.head.commit.hexsha
        run["gitremotes"] = get_remotes(repo)

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


# The released version of PySvn doesn't do local diffs yet, so we have to do
# it the hard way...
class SvnException(Exception):
    pass


def svn_diff(path):
    """
    Run svn diff for the given path and return the result. Raise SvnException
    if the command doesn't return 0.
    """
    cmd = ["svn", "diff", path]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env={"LANG": "en_US.UTF-8"})
    stdout = p.stdout.read()
    r = p.wait()
    if r != 0:
        raise SvnException("SVN Command exited with status code {0}".format(r))
    return stdout.decode()


def add_svn_info(run, scriptpath):
    """
    Add information about the svn repository holding the source file to the
    database.
    """
    try:
        svn_client = svn.local.LocalClient(scriptpath)
        svn_info = svn_client.info()
        run["svnrepo"] = svn_info["repository_root"]
        run["svncommit"] = svn_info["commit_revision"]
        if not option_set('ignored metadata', 'diff'):
            run['diff'] = svn_diff(svn_info["wc-info/wcroot-abspath"])
    except (svn.exception.SvnException, ValueError, OSError):
        # We can't access svn info for some reason, so just skip it
        pass
