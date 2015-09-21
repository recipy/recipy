# Change Log

## [v0.2.0](https://github.com/recipy/recipy/tree/v0.2.0) (2015-09-21)
[Full Changelog](https://github.com/recipy/recipy/compare/v0.1.0...v0.2.0)

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







