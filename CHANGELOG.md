# Change Log

## [Unreleased](https://github.com/recipy/recipy/tree/HEAD)
This was released after recipy was revealed to the world at EuroSciPy 2015. The major feature additions were:

- Blah
- Something else

[Full Changelog](https://github.com/recipy/recipy/compare/v0.1.0...HEAD)

**Fixed bugs:**

- Config file reading doesn't work as specified in the docs [\#64](https://github.com/recipy/recipy/issues/64)
- Not all pandas output methods are wrapped [\#11](https://github.com/recipy/recipy/issues/11)

**Closed issues:**

- recipyCommon is not a package [\#62](https://github.com/recipy/recipy/issues/62)
- Make proper documentation about config file options [\#60](https://github.com/recipy/recipy/issues/60)
- Add 'latest' option to CLI [\#59](https://github.com/recipy/recipy/issues/59)
- Make DB path configurable [\#57](https://github.com/recipy/recipy/issues/57)
- Configuration option not to track input or output files [\#56](https://github.com/recipy/recipy/issues/56)
- Log sys.argv [\#54](https://github.com/recipy/recipy/issues/54)
- Configuration file should be ~/.recipy/recipyrc [\#46](https://github.com/recipy/recipy/issues/46)
- Add 'quiet' option to config file to stop display of 'recipy run inserted xyz' message [\#43](https://github.com/recipy/recipy/issues/43)
- GUI Internal Server Error when viewing run with no git metadata [\#42](https://github.com/recipy/recipy/issues/42)
- keeping track of in- and outfile versions [\#41](https://github.com/recipy/recipy/issues/41)
- Logging of parameters [\#40](https://github.com/recipy/recipy/issues/40)
- Convert to use TinyDB [\#39](https://github.com/recipy/recipy/issues/39)
- Add 'command' functionality to recipy-cmd [\#37](https://github.com/recipy/recipy/issues/37)
- Create text index on all fields in database [\#35](https://github.com/recipy/recipy/issues/35)
- Make compatible with Python 3 \(and still with Python 2\) [\#34](https://github.com/recipy/recipy/issues/34)
- Add configuration file support [\#33](https://github.com/recipy/recipy/issues/33)
- Add working setup.py [\#31](https://github.com/recipy/recipy/issues/31)
- Deal with git status of multiple files [\#29](https://github.com/recipy/recipy/issues/29)
- Use PyMongo v3? [\#28](https://github.com/recipy/recipy/issues/28)
- Add fuzzy searching option to recipy-cmd [\#27](https://github.com/recipy/recipy/issues/27)
- Make recipy-cmd work to search for full paths when given file in current directory [\#26](https://github.com/recipy/recipy/issues/26)
- Store diffs between script as executed and latest git commit [\#24](https://github.com/recipy/recipy/issues/24)
- Upload to PyPI [\#23](https://github.com/recipy/recipy/issues/23)
- Add hooks for scikit-learn [\#16](https://github.com/recipy/recipy/issues/16)
- Add hooks for scikit-image [\#15](https://github.com/recipy/recipy/issues/15)
- Add hooks for scikit-image [\#14](https://github.com/recipy/recipy/issues/14)
- Add hooks for PIL and Pillow [\#13](https://github.com/recipy/recipy/issues/13)
- Add recipy-cmd function to create DB and set text index [\#10](https://github.com/recipy/recipy/issues/10)
- Get more details on the environment and store in the DB [\#9](https://github.com/recipy/recipy/issues/9)
- Add a way to share entries from the DB [\#8](https://github.com/recipy/recipy/issues/8)
- Add interfaces from more languages and other tools [\#7](https://github.com/recipy/recipy/issues/7)
- Keep track of git commit version of script [\#6](https://github.com/recipy/recipy/issues/6)
- Add automatic installation for various OS's [\#5](https://github.com/recipy/recipy/issues/5)
- Add proper setup.py file [\#4](https://github.com/recipy/recipy/issues/4)
- Add hooks for more commonly-used Python modules [\#3](https://github.com/recipy/recipy/issues/3)
- Store full paths to files [\#2](https://github.com/recipy/recipy/issues/2)
- Make recipy-cmd search with fuzzy matches [\#1](https://github.com/recipy/recipy/issues/1)

**Merged pull requests:**

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







