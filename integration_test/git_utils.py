"""
Functions to provide information about a Git repository.
"""

from __future__ import (nested_scopes, generators, division,
                        absolute_import, with_statement,
                        print_function, unicode_literals)

import hashlib
import os
from git import Repo
from git.exc import InvalidGitRepositoryError


BLOCKSIZE = 65536


def hash_file(path):
    """
    Get hash of file, where:

    :param path: file path
    :type path: str or unicode
    :return: hash or None if the file does not exist
    :rtype: str or unicode
    """
    try:
        hasher = hashlib.sha1()
        with open(path, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()
    except Exception:
        return None


def get_repository(file_path):
    """
    Get repository object for repository within which given file
    is located.

    :param file_path: File path
    :type file_path: str or unicode
    :return: repository or None if no repository can be found
    :rtype: git.Repo
    :raises git.exc.NoSuchPathError: if the path does not exist
    """
    path = os.path.realpath(file_path)
    repository = None
    try:
        repository = Repo(path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        pass
    return repository


def get_repository_path(repository):
    """
    Get local repository path.

    :param repository: repository
    :type repository: git.Repo
    :return: repository path
    :rtype: str or unicode
    """
    return repository.working_dir


def get_commit(repository):
    """
    Get current commit ID.

    :param repository: repository
    :type repository: git.Repo
    :return: commit ID
    :rtype: str or unicode
    """
    return repository.head.commit.hexsha


def get_origin(repository):
    """
    Get current repository origin.

    :param repository: repository
    :type repository: git.Repo
    :return: origin URL
    :rtype: str or unicode
    """
    return repository.remotes.origin.url


def get_remote(repository, remote):
    """
    Get current repository remote.

    :param repository: repository
    :type repository: git.Repo
    :param remote: remote name
    :type remote: str or unicode
    :return: remote URL or None if no such remote
    :rtype: str or unicode
    """
    remote_url = None
    try:
        remote_url = repository.remotes[remote].url
    except IndexError:
        pass
    return remote_url
