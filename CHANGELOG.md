# Change Log

## [v0.3.0](https://github.com/recipy/recipy/tree/v0.3.0) (2016-09-13)
[Full Changelog](https://github.com/recipy/recipy/compare/v0.2.3...v0.3.0)

This is a major release with a number of new features and lots of tidying up. It has been released in time for PyConUK, where we will be sprinting on recipy and hopefully developing even more new features and fixing more bugs.

The major new features are:

 * A hash is now computed for all input and output files, and this is used for searching for files. Practically, this means that you can create `graph.png`, send it to a colleague, and even if they send back a file called `RobinsGraph.png` you can still look up how it was created, as the hash will be the same even if the filename isn't.
 * Hashes are computed by default, rather than hashing having to be switched on in the config file (Note: this is a change from the pre-release versions, as hashing is now working effectively).
 * `recipy search` has gained a new option: `--filepath` (or `-p`) which forces searching based on the file and path rather than the hash.
 * There is now a beta-quality `recipy.open` function that can be used instead of Python's standard `open` function to log files that are opened. (The reason why the standard Python `open` command can't be wrapped by recipy is a topic for a blog post, I think). There are some known issues with this function, but it should work for many use cases.
 * Versions of the libraries that are patched by recipy are now stored with the run
 * There is now a `recipy annotate` command that can be used to add notes to a 'recipy run'.
 * There is a new tab in the GUI that lists all of modules and functions that are patched by this version of recipy.
 * The terminal output from the `recipy` command is now far more easy to read, as it uses different font styles for headers and the actual content
 * The GUI has been updated to handle and display all of the new information we're storing.
 * Lots of bugs have been fixed (far more than listed in the issues below, as not all were recorded officially via issues) and the `recipy search` command is far more robust now.

 Huge thanks must also go to [mikej888](https://github.com/mikej888) who has been working on recipy through the [Software Sustainability Institute](http://www.software.ac.uk) and has reported many bugs and give lots of ideas for improvements. He is currently working on a test suite that should make the whole package far more robust.

**Implemented enhancements:**

- Store hash for input/output files [\#25](https://github.com/recipy/recipy/issues/25)
- Hook into standard `open` etc in pure python [\#44](https://github.com/recipy/recipy/issues/44)
- Store data diffs [\#107](https://github.com/recipy/recipy/issues/107)
- Format terminal output nicely [\#102](https://github.com/recipy/recipy/issues/102)
- How should GUI display hashes? [\#100](https://github.com/recipy/recipy/issues/100)
- Store versions of libraries used [\#87](https://github.com/recipy/recipy/issues/87)
- Use colours in terminal output of CLI [\#86](https://github.com/recipy/recipy/issues/86)
- Add 'annotate' functionality [\#69](https://github.com/recipy/recipy/issues/69)

**Fixed bugs:**

- Output to JSON with no results found fails with IndexError [\#142](https://github.com/recipy/recipy/issues/142)
- recipy command fails on Windows due to blessings use [\#141](https://github.com/recipy/recipy/issues/141)
- Issues with searching by ID [\#124](https://github.com/recipy/recipy/issues/124)
- latest\_run throws an error if there are no runs in the database [\#118](https://github.com/recipy/recipy/issues/118)
- tinydb error [\#92](https://github.com/recipy/recipy/issues/92)
- Recipy not able to find a file  [\#89](https://github.com/recipy/recipy/issues/89)
- Add blessings to setup.py [\#140](https://github.com/recipy/recipy/issues/140)
- Diffs can't be applied as patches because no filename info is included [\#133](https://github.com/recipy/recipy/issues/133)
- matplotlib isn't a dependency [\#115](https://github.com/recipy/recipy/issues/115)
- TypeError: 'Query' object is not callable when searching for runs in GUI [\#112](https://github.com/recipy/recipy/issues/112)

**Closed issues:**

- Split the GUI into a separate PyPI package? [\#117](https://github.com/recipy/recipy/issues/117)
- Use with R via doit? [\#114](https://github.com/recipy/recipy/issues/114)
- Source code not PEP-8 [\#110](https://github.com/recipy/recipy/issues/110)
- Python 3 compatibility: deprecated modules [\#109](https://github.com/recipy/recipy/issues/109)

**Merged pull requests:**

- adds check for $EDITOR for the annotate command [\#97](https://github.com/recipy/recipy/pull/97) ([cash](https://github.com/cash))
- updated readme to be consistent about location of recipy console script [\#96](https://github.com/recipy/recipy/pull/96) ([cash](https://github.com/cash))
- add test\_requirements.txt for installing unit test dependencies [\#94](https://github.com/recipy/recipy/pull/94) ([cash](https://github.com/cash))
- adds tinydb-serialization to requirements.txt for manually installing deps [\#93](https://github.com/recipy/recipy/pull/93) ([cash](https://github.com/cash))


## [v0.2.3](https://github.com/recipy/recipy/tree/HEAD)
[Full Changelog](https://github.com/recipy/recipy/compare/v0.2.3...HEAD)

This is a very small release to fix recipy to work with the latest version of TinyDB (v3.0.0).

**Fixed bugs:**

- TinyDB import error [\#92](https://github.com/recipy/recipy/issues/92)

## [v0.2.1](https://github.com/recipy/recipy/tree/v0.2.1)
[Full Changelog](https://github.com/recipy/recipy/compare/v0.2.0...HEAD)

Minor bug-fix release.

**Fixed bugs:**

- Patching of Pillow does not work due to [\#52](https://github.com/recipy/recipy/issues/52), which caused matplotlib imports to fail. Fixed by removing Pillow support for the moment

## [v0.2.0](https://github.com/recipy/recipy/tree/v0.2.0) (2015-09-21)
[Full Changelog](https://github.com/recipy/recipy/compare/v0.1.0...v0.2.0)

This is the first new release of recipy since its debut at EuroSciPy 2015. Sorry for the delay in getting this out, life has been rather chaotic for all of the members of the recipy team. We want to say a huge thank you to all of the people who have submitted issues and pull requests: we couldn't have done this without you!

Full details are below, but the major new features include logging command-line arguments, exporting runs to JSON, adding more configuration options, and adding more commands to the GUI. A number of bugs have also been fixed.

**Implemented enhancements:**

- Add export option to the GUI [\#68](https://github.com/recipy/recipy/issues/68)
- Add 'latest' option to CLI [\#59](https://github.com/recipy/recipy/issues/59)
- Make DB path configurable [\#57](https://github.com/recipy/recipy/issues/57)
- Configuration option not to track input or output files [\#56](https://github.com/recipy/recipy/issues/56)
- Add search by id [\#49](https://github.com/recipy/recipy/issues/49)
- Configuration file should be ~/.recipy/recipyrc [\#46](https://github.com/recipy/recipy/issues/46)
- Add 'quiet' option to config file to stop display of 'recipy run inserted xyz' message [\#43](https://github.com/recipy/recipy/issues/43)
- Add export of individual runs, or the whole database [\#50](https://github.com/recipy/recipy/issues/50)
- Log command-line arguments [\#47](https://github.com/recipy/recipy/issues/47)

**Fixed bugs:**

- Loading a numpy file gives error message, only after recipy import. [\#83](https://github.com/recipy/recipy/issues/83)
- Config file reading doesn't work as specified in the docs [\#64](https://github.com/recipy/recipy/issues/64)
- recipyCommon is not a package [\#62](https://github.com/recipy/recipy/issues/62)

**Closed issues:**

- GUI port number consistency [\#80](https://github.com/recipy/recipy/issues/80)
- README.md example is inconsistent [\#78](https://github.com/recipy/recipy/issues/78)
- Make UTC explicit in interfaces [\#75](https://github.com/recipy/recipy/issues/75)
- Tidy up inputs/outputs lists when there are none of them [\#74](https://github.com/recipy/recipy/issues/74)
- Add release notes [\#67](https://github.com/recipy/recipy/issues/67)
- Make proper documentation about config file options [\#60](https://github.com/recipy/recipy/issues/60)
- GUI Internal Server Error when viewing run with no git metadata [\#42](https://github.com/recipy/recipy/issues/42)
- keeping track of in- and outfile versions [\#41](https://github.com/recipy/recipy/issues/41)
- Logging of parameters [\#40](https://github.com/recipy/recipy/issues/40)
- Convert to use TinyDB [\#39](https://github.com/recipy/recipy/issues/39)
- Add 'command' functionality to recipy-cmd [\#37](https://github.com/recipy/recipy/issues/37)
- Create text index on all fields in database [\#35](https://github.com/recipy/recipy/issues/35)
- Upload to PyPI [\#23](https://github.com/recipy/recipy/issues/23)
- Add recipy-cmd function to create DB and set text index [\#10](https://github.com/recipy/recipy/issues/10)

**Merged pull requests:**

- GUI port number [\#81](https://github.com/recipy/recipy/pull/81) ([sjdenny](https://github.com/sjdenny))
- Add python highlighting in the README.md [\#79](https://github.com/recipy/recipy/pull/79) ([musically-ut](https://github.com/musically-ut))
- fixed typo in modulename of PatchPillow [\#73](https://github.com/recipy/recipy/pull/73) ([MichielCottaar](https://github.com/MichielCottaar))
- Command args [\#71](https://github.com/recipy/recipy/pull/71) ([oew1v07](https://github.com/oew1v07))
- Allow running recipy as a module \(python -m recipy\) [\#66](https://github.com/recipy/recipy/pull/66) ([kynan](https://github.com/kynan))
- Nibabel support [\#51](https://github.com/recipy/recipy/pull/51) ([MichielCottaar](https://github.com/MichielCottaar))

## [v0.1.0](https://github.com/recipy/recipy/tree/v0.1.0) (2015-08-16)

This is the first public release of recipy. The changes listed below are compared to early pre-release versions.

**Fixed bugs:**

- Not all pandas output methods are wrapped [\#11](https://github.com/recipy/recipy/issues/11)

**Closed issues:**

- Make compatible with Python 3 \(and still with Python 2\) [\#34](https://github.com/recipy/recipy/issues/34)
- Add configuration file support [\#33](https://github.com/recipy/recipy/issues/33)
- Add working setup.py [\#31](https://github.com/recipy/recipy/issues/31)
- Deal with git status of multiple files [\#29](https://github.com/recipy/recipy/issues/29)
- Use PyMongo v3? [\#28](https://github.com/recipy/recipy/issues/28)
- Add fuzzy searching option to recipy-cmd [\#27](https://github.com/recipy/recipy/issues/27)
- Make recipy-cmd work to search for full paths when given file in current directory [\#26](https://github.com/recipy/recipy/issues/26)
- Store diffs between script as executed and latest git commit [\#24](https://github.com/recipy/recipy/issues/24)
- Add hooks for scikit-learn [\#16](https://github.com/recipy/recipy/issues/16)
- Add hooks for scikit-image [\#15](https://github.com/recipy/recipy/issues/15)
- Add hooks for scikit-image [\#14](https://github.com/recipy/recipy/issues/14)
- Add hooks for PIL and Pillow [\#13](https://github.com/recipy/recipy/issues/13)
- Get more details on the environment and store in the DB [\#9](https://github.com/recipy/recipy/issues/9)
- Add a way to share entries from the DB [\#8](https://github.com/recipy/recipy/issues/8)
- Add interfaces from more languages and other tools [\#7](https://github.com/recipy/recipy/issues/7)
- Keep track of git commit version of script [\#6](https://github.com/recipy/recipy/issues/6)
- Add automatic installation for various OS's [\#5](https://github.com/recipy/recipy/issues/5)
- Add proper setup.py file [\#4](https://github.com/recipy/recipy/issues/4)
- Add hooks for more commonly-used Python modules [\#3](https://github.com/recipy/recipy/issues/3)
- Store full paths to files [\#2](https://github.com/recipy/recipy/issues/2)
- Make recipy-cmd search with fuzzy matches [\#1](https://github.com/recipy/recipy/issues/1)
