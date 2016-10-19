"""
recipy-related regexps.
"""

# Copyright (c) 2016 University of Edinburgh.


def get_usage():
    """
    Get regular expressions for usage information printed to console.

    :returns: regular expressions
    :rtype: list of str or unicode
    """
    return [r"Usage:\n"]


def get_version():
    """
    Get regular expressions for version information printed to
    console.

    :returns: regular expressions
    :rtype: list of str or unicode
    """
    return [r"recipy v[0-9]\.[0-9]\.[0-9]"]


def get_help():
    """
    Get regular expressions for help information printed to
    console.

    :returns: regular expressions
    :rtype: list of str or unicode
    """
    return [r"recipy - a frictionless provenance tool for Python\n",
            r"Usage:\n",
            r"Options:\n"]


def get_debug_recipy():
    """
    Get regular expressions for debug information printed to
    console.

    :returns: regular expressions
    :rtype: list of str or unicode
    """
    return [r"Command-line arguments: \n",
            r"DB path: .*\n",
            r"Full config file \(as interpreted\):\n",
            r"----------------------------------\n",
            r"----------------------------------\n"]


def get_db_empty():
    """
    Get regular expressions for information printed to console, when
    recipy database is empty.

    :returns: regular expressions
    :rtype: list of str or unicode
    """
    return [r"Database is empty"]


def get_stdout(log):
    """
    Get regular expressions for recipy log information printed to
    console.

    :param log: Recipy database log
    :type log: dict
    :returns: regular expressions
    :rtype: list of str or unicode
    """
    return [r"Run ID: " + log["unique_id"] + "\n",
            r"Created by " + log["author"] + " on .*\n",
            r"Ran " + log["script"].replace("\\", "\\\\") +
            " using .*\n",
            r"Git: commit " + log["gitcommit"] + ", in repo " +
            log["gitrepo"].replace("\\", "\\\\") +
            ", with origin " + str(log["gitorigin"]) + ".*\n",
            r"Environment: .*\n",
            r"Libraries: " + ", ".join(log["libraries"]) + "\n",
            r"Inputs:\n",
            log["inputs"][0][0].replace("\\", "\\\\"),
            log["inputs"][0][1],
            log["inputs"][0][0].replace("\\", "\\\\") +
            r" \(" + log["inputs"][0][1] + r"\)\n",
            r"Outputs:\n",
            log["outputs"][0][0].replace("\\", "\\\\") +
            r" \(" + log["outputs"][0][1] + r"\)\n"]


def get_diff(script):
    """
    Get regular expressions for recipy "diff"-related log information
    printed to console and recorded in database.

    This function assumes that the only change made to a file was the
    addition of a line with text "pass".

    :param script: script for which diff information was logged
    :type script: str or unicode
    :returns: regular expressions
    :rtype: list of str or unicode
    """
    return [
        r"---.*" + script + "\n",
        r"\+\+\+.*" + script + "\n",
        r"@@.*\n",
        r"\+pass.*\n"]


def get_no_results():
    """
    Get regular expressions for information printed to console, when
    there are no results for a search.

    :returns: regular expressions
    :rtype: list of str or unicode
    """
    return [r"No results found"]


def get_debug():
    """
    Get regular expressions for debug information printed to console.
    This function assumes that the script invokes an input function and
    an output function.

    :returns: regular expressions
    :rtype: list of str or unicode
    """
    return [r"recipy run inserted",
            r"Patching",
            r"Patching input function",
            r"Patching output function",
            r"Input from",
            r"Output to",
            r"recipy run complete"]


def get_filediffs():
    """
    Get regular expressions for recipy "filediffs"-related log
    information recorded in database.

    :returns: regular expressions
    :rtype: list of str or unicode
    """
    return [r"before this run", r"after this run"]
