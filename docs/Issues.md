# recipy and third-party package issues

Issues encountered during test framework development and how the test
framework has been configured to get round these issues.

## No information logged by recipy (recipy code is commented-out)

All these tests are marked as skipped.

### `PIL` operations

To replicate:

```
python -m integration_test.packages.run_pil image_open
recipy latest
```
```
Run ID: cf695a6c-e9f0-4f4b-896f-9fa64127e2e8
Created by ubuntu on 2016-10-26 11:59:04 UTC
Ran /home/ubuntu/recipy/integration_test/packages/run_pil.py using /home/ubuntu/anaconda2/bin/python
Using command-line arguments: image_open
Git: commit 5dc58a3cf3432441c83fd9899768eb9b63583208, in repo /home/ubuntu/recipy, with origin https://mikej888@github.com/mikej888/recipy
Environment: Linux-3.19.0-25-generic-x86_64-with-debian-jessie-sid, python 2.7.12 |Anaconda custom (64-bit)| (default, Jul  2 2016, 17:42:40)
Libraries: recipy v0.3.0
Inputs: none
Outputs: none
```

### `skimage` operations

To replicate:

```
python -m integration_test.packages.run_skimage io_imread
recipy latest
```

```
Run ID: 10c803f7-3741-4008-8548-2f8d7ba4462c
Created by ubuntu on 2016-10-26 11:57:07 UTC
Ran /home/ubuntu/recipy/integration_test/packages/run_skimage.py using /home/ubuntu/anaconda2/bin/python
Using command-line arguments: io_imread
Git: commit 5dc58a3cf3432441c83fd9899768eb9b63583208, in repo /home/ubuntu/recipy, with origin https://mikej888@github.com/mikej888/recipy
Environment: Linux-3.19.0-25-generic-x86_64-with-debian-jessie-sid, python 2.7.12 |Anaconda custom (64-bit)| (default, Jul  2 2016, 17:42:40)
Libraries: recipy v0.3.0
Inputs: none
Outputs: none
```

---

## Inaccurate information logged by recipy

## Bugs arising within recipy logging

All these tests are marked as skipped.

### `recipy.open`

To replicate:

```
python -m integration_test.packages.run_python open
```

Under Python 3 this fails with:

```
recipy run inserted, with ID 9abe4113-5158-4dcb-8fe8-afd1b1f6505e

Traceback (most recent call last):
  File "c:\Users\mjj\AppData\Local\Continuum\Anaconda3\lib\runpy.py", line 170,in _run_module_as_main
    "__main__", mod_spec)
  File "c:\Users\mjj\AppData\Local\Continuum\Anaconda3\lib\runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "c:\Users\mjj\Local Documents\recipy\recipy\integration_test\packages\run_python.py", line 45, in <module>
    PythonSample().invoke(sys.argv)
  File "c:\Users\mjj\Local Documents\recipy\recipy\integration_test\packages\base.py", line 57, in invoke
    function()
  File "c:\Users\mjj\Local Documents\recipy\recipy\integration_test\packages\run_python.py", line 39, in open
    with recipy.open('out.txt', 'w') as f:
  File "c:\Users\mjj\Local Documents\recipy\recipy\recipy\utils.py", line 20, in open
    mode = kwargs['mode']
KeyError: 'mode'
```

Under Python 2 this fails with:

```
recipy run inserted, with ID 5d80b88b-0d56-428d-b9e0-d95eca423044

Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/home/ubuntu/recipy/integration_test/packages/run_python.py", line 42, in <module>
    python_sample.invoke(sys.argv)
  File "integration_test/packages/base.py", line 57, in invoke
    function()
  File "/home/ubuntu/recipy/integration_test/packages/run_python.py", line 35, in open
    with recipy.open('out.txt', 'w') as f:
  File "recipy/utils.py", line 35, in open
    log_output(args[0], 'recipy.open')
  File "recipy/log.py", line 153, in log_output
    db.update(append("libraries", get_version(source), no_duplicates=True), eids=[RUN_ID])
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 377, in update
    cond, eids
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 230, in process_elements
    data = self._read()
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 277, in _read
    return self._storage.read()
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 31, in read
    raw_data = (self._storage.read() or {})[self._table_name]
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb_serialization/__init__.py", line 139, in read
    data = self.storage.read()
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/storages.py", line 93, in read
    self._handle.seek(0, 2)
ValueError: I/O operation on closed file
```

### `bs4.beautifulsoup.prettify`

To replicate:

```
python -m integration_test.packages.run_bs4 beautifulsoup
```
```
Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/home/ubuntu/recipy/integration_test/packages/run_bs4.py", line 53, in <module>
    Bs4Sample().invoke(sys.argv)
  File "integration_test/packages/base.py", line 57, in invoke
    function()
  File "/home/ubuntu/recipy/integration_test/packages/run_bs4.py", line 49, in beautifulsoup
    print((soup.prettify()))
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/bs4/element.py", line 1160, in prettify
    return self.decode(True, formatter=formatter)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/bs4/__init__.py", line 439, in decode
    return prefix + super(BeautifulSoup, self).decode(
TypeError: super() argument 1 must be type, not FunctionWrapper
```

### `pandas.Panel.to_excel`

To replicate:

```
python -m integration_test.packages.run_pandas panel_to_excel
```
```
Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/home/ubuntu/recipy/integration_test/packages/run_pandas.py", line 355, in <module>
    PandasSample().invoke(sys.argv)
  File "integration_test/packages/base.py", line 57, in invoke
    function()
  File "/home/ubuntu/recipy/integration_test/packages/run_pandas.py", line 195, in panel_to_excel
    panel.to_excel(file_name)
  File "recipyCommon/utils.py", line 91, in f
    return wrapped(*args, **kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/pandas/core/panel.py", line 460, in to_excel
    df.to_excel(writer, name, **kwargs)
  File "recipyCommon/utils.py", line 90, in f
    function(args[arg_loc], source)
  File "recipy/log.py", line 139, in log_output
    filename = os.path.abspath(filename)
  File "/home/ubuntu/anaconda2/lib/python2.7/posixpath.py", line 360, in abspath
    if not isabs(path):
  File "/home/ubuntu/anaconda2/lib/python2.7/posixpath.py", line 54, in isabs
    return s.startswith('/')
AttributeError: '_XlwtWriter' object has no attribute 'startswith'
```

### `nibabel.minc2.Minc2Image.from_filename`

To replicate:

```
python -m integration_test.packages.run_nibabel minc2_from_filename
```
```
Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/home/ubuntu/recipy/integration_test/packages/run_nibabel.py", line 302, in <module>
    NibabelSample().invoke(sys.argv)
  File "integration_test/packages/base.py", line 57, in invoke
    function()
  File "/home/ubuntu/recipy/integration_test/packages/run_nibabel.py", line 143, in minc2_from_filename
    data = nib.minc2.Minc2Image.from_filename(file_name)
  File "recipyCommon/utils.py", line 91, in f
    return wrapped(*args, **kwargs)
  File "recipyCommon/utils.py", line 91, in f
    return wrapped(*args, **kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/spatialimages.py", line 699, in from_filename
    return klass.from_file_map(file_map)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/minc1.py", line 299, in from_file_map
    minc_file = Minc1File(netcdf_file(fobj))
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/externals/netcdf.py", line 230, in __init__
    self._read()
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/externals/netcdf.py", line 513, in _read
    self.filename)
TypeError: Error: None is not a valid NetCDF 3 file
```

### `nibabel.Nifti2Image.from_filename`

To replicate:

```
python -m integration_test.packages.run_nibabel nifti2_from_filename
```
```
sizeof_hdr should be 348; set sizeof_hdr to 348
data code 0 not supported; not attempting fix
Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/home/ubuntu/recipy/integration_test/packages/run_nibabel.py", line 302, in <module>
    NibabelSample().invoke(sys.argv)
  File "integration_test/packages/base.py", line 57, in invoke
    function()
  File "/home/ubuntu/recipy/integration_test/packages/run_nibabel.py", line 182, in nifti2_from_filename
    data = nib.Nifti2Image.from_filename(file_name)
  File "recipyCommon/utils.py", line 91, in f
    return wrapped(*args, **kwargs)
  File "recipyCommon/utils.py", line 91, in f
    return wrapped(*args, **kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/keywordonly.py", line 16, in wrapper
    return func(*args, **kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/analyze.py", line 986, in from_filename
    return klass.from_file_map(file_map, mmap=mmap)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/keywordonly.py", line 16, in wrapper
    return func(*args, **kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/analyze.py", line 947, in from_file_map
    header = klass.header_class.from_fileobj(hdrf)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/nifti1.py", line 594, in from_fileobj
    hdr = klass(raw_str, endianness, check)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/nifti1.py", line 577, in __init__
    check)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/analyze.py", line 252, in __init__
    super(AnalyzeHeader, self).__init__(binaryblock, endianness, check)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/wrapstruct.py", line 176, in __init__
    self.check_fix()
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/wrapstruct.py", line 361, in check_fix
    report.log_raise(logger, error_level)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/batteryrunners.py", line 275, in log_raise
    raise self.error(self.problem_msg)
nibabel.spatialimages.HeaderDataError: data code 0 not supported
```

### `sklearn.load_svmlight_file` and `sklearn.dump_svmlight_file`

To replicate:

```
python -m integration_test.packages.run_sklearn load_svmlight_file
```

Under Python 3 this fails with:

```
Traceback (most recent call last):
  File "/home/ubuntu/anaconda3/lib/python3.5/runpy.py", line 184, in _run_module_as_main
    "__main__", mod_spec)
  File "/home/ubuntu/anaconda3/lib/python3.5/runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "/home/ubuntu/recipy/integration_test/packages/run_sklearn.py", line 16, in <module>
    from sklearn import datasets
  File "<frozen importlib._bootstrap>", line 969, in _find_and_load
  File "<frozen importlib._bootstrap>", line 958, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 664, in _load_unlocked
  File "<frozen importlib._bootstrap>", line 634, in _load_backward_compatible
  File "/home/ubuntu/recipy/recipy/PatchImporter.py", line 52, in load_module
    mod = self.patch(mod)
  File "/home/ubuntu/recipy/recipy/PatchSimple.py", line 25, in patch
    patch_function(mod, f, self.input_wrapper)
  File "/home/ubuntu/recipy/recipyCommon/utils.py", line 82, in patch_function
    setattr(mod, old_f_name, recursive_getattr(mod, function))
  File "/home/ubuntu/recipy/recipyCommon/utils.py", line 54, in recursive_getattr
    prev_part = getattr(prev_part, part)
AttributeError: module 'sklearn' has no attribute 'datasets'
```

Under Python 2 this fails with:

```
Traceback (most recent call last):
  File "recipy/log.py", line 165, in log_exception
    db.update({"exception": exception}, eids=[RUN_ID])
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 382, in update
    cond, eids
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 235, in process_elements
    func(data, eid)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 381, in <lambda>
    lambda data, eid: data[eid].update(fields),
KeyError: 316

Original exception was:
Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/home/ubuntu/recipy/integration_test/packages/run_sklearn.py", line 16, in <module>
    from sklearn import datasets
  File "recipy/PatchImporter.py", line 52, in load_module
    mod = self.patch(mod)
  File "recipy/PatchSimple.py", line 25, in patch
    patch_function(mod, f, self.input_wrapper)
  File "recipyCommon/utils.py", line 82, in patch_function
    setattr(mod, old_f_name, recursive_getattr(mod, function))
  File "recipyCommon/utils.py", line 54, in recursive_getattr
    prev_part = getattr(prev_part, part)
AttributeError: 'module' object has no attribute 'datasets'
Error in atexit._run_exitfuncs:
Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
    func(*targs, **kargs)
  File "recipy/log.py", line 244, in hash_outputs
    for filename in run.get('outputs')]
AttributeError: 'NoneType' object has no attribute 'get'
Error in atexit._run_exitfuncs:
Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
    func(*targs, **kargs)
  File "recipy/log.py", line 231, in log_exit
    db.update({'exit_date': exit_date}, eids=[RUN_ID])
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 382, in update
    cond, eids
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 235, in process_elements
    func(data, eid)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 381, in <lambda>
    lambda data, eid: data[eid].update(fields),
KeyError: 316
Error in sys.exitfunc:
Error in sys.excepthook:
Traceback (most recent call last):
  File "recipy/log.py", line 165, in log_exception
    db.update({"exception": exception}, eids=[RUN_ID])
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 382, in update
    cond, eids
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 235, in process_elements
    func(data, eid)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 381, in <lambda>
    lambda data, eid: data[eid].update(fields),
KeyError: 316

Original exception was:
Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
    func(*targs, **kargs)
  File "recipy/log.py", line 231, in log_exit
    db.update({'exit_date': exit_date}, eids=[RUN_ID])
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 382, in update
    cond, eids
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 235, in process_elements
    func(data, eid)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/tinydb/database.py", line 381, in <lambda>
    lambda data, eid: data[eid].update(fields),
KeyError: 316
```

---

## Operations not implemented by packages

All these tests are marked as skipped.

### `nibabel.minc1.Minc1Image.to_filename`

To replicate:

```
python -m integration_test.packages.run_nibabel minc1_to_filename
```
```
Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/home/ubuntu/recipy/integration_test/packages/run_nibabel.py", line 302, in <module>
    NibabelSample().invoke(sys.argv)
  File "integration_test/packages/base.py", line 57, in invoke
    function()
  File "/home/ubuntu/recipy/integration_test/packages/run_nibabel.py", line 134, in minc1_to_filename
    img.to_filename(file_name)
  File "recipyCommon/utils.py", line 91, in f
    return wrapped(*args, **kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/spatialimages.py", line 781, in to_filename
    self.to_file_map()
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/spatialimages.py", line 790, in to_file_map
    raise NotImplementedError
NotImplementedError
```

### `nibabel.minc2.Minc2Image.to_filename`

To replicate:

```
python -m integration_test.packages.run_nibabel minc2_to_filename
```
```
Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/home/ubuntu/recipy/integration_test/packages/run_nibabel.py", line 302, in <module>
    NibabelSample().invoke(sys.argv)
  File "integration_test/packages/base.py", line 57, in invoke
    function()
  File "/home/ubuntu/recipy/integration_test/packages/run_nibabel.py", line 154, in minc2_to_filename
    img.to_filename(file_name)
  File "recipyCommon/utils.py", line 91, in f
    return wrapped(*args, **kwargs)
  File "recipyCommon/utils.py", line 91, in f
    return wrapped(*args, **kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/spatialimages.py", line 781, in to_filename
    self.to_file_map()
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/spatialimages.py", line 790, in to_file_map
    raise NotImplementedError
NotImplementedError
```

### `nibabel.parrec.PARRECImage.to_filename`

To replicate:

```
python -m integration_test.packages.run_nibabel parrec_to_filename
```
```
Traceback (most recent call last):
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 174, in _run_module_as_main
    "__main__", fname, loader, pkg_name)
  File "/home/ubuntu/anaconda2/lib/python2.7/runpy.py", line 72, in _run_code
    exec code in run_globals
  File "/home/ubuntu/recipy/integration_test/packages/run_nibabel.py", line 302, in <module>
    NibabelSample().invoke(sys.argv)
  File "integration_test/packages/base.py", line 57, in invoke
    function()
  File "/home/ubuntu/recipy/integration_test/packages/run_nibabel.py", line 217, in parrec_to_filename
    img.to_filename(par_file_name)
  File "recipyCommon/utils.py", line 91, in f
    return wrapped(*args, **kwargs)
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/spatialimages.py", line 781, in to_filename
    self.to_file_map()
  File "/home/ubuntu/anaconda2/lib/python2.7/site-packages/nibabel/spatialimages.py", line 790, in to_file_map
    raise NotImplementedError
NotImplementedError
```

---

## Using py.test and recipy

An issue that does not affect the test framework, but may affect
future test development is that recipy and py.test do not
integrate. For example, given test_sample.py:

```
class TestSample:

    def test_sample(self):
        pass
```

Running:

```
py.test test_sample.py
```

gives:

```
============================= test session starts =============================
platform win32 -- Python 3.5.1, pytest-3.0.2, py-1.4.31, pluggy-0.3.1
rootdir: c:\Users\mjj\Local Documents, inifile:
collected 1 items

test_sample.py .

========================== 1 passed in 0.02 seconds ===========================
```

Adding:

```
import recipy
```

Running py.test gives:

```
============================= test session starts =============================
platform win32 -- Python 3.5.1, pytest-3.0.2, py-1.4.31, pluggy-0.3.1
rootdir: c:\Users\mjj\Local Documents, inifile:
collected 0 items / 1 errors

=================================== ERRORS ====================================
_______________________ ERROR collecting test_sample.py _______________________
..\appdata\local\continuum\anaconda3\lib\site-packages\_pytest\python.py:209: in fget
    return self._obj
E   AttributeError: 'Module' object has no attribute '_obj'

During handling of the above exception, another exception occurred:
test_sample.py:1: in <module>
    import recipy
..\appdata\local\continuum\anaconda3\lib\site-packages\recipy-0.3.0-py3.5.egg\recipy\__init__.py:12: in <module>
    log_init()
..\appdata\local\continuum\anaconda3\lib\site-packages\recipy-0.3.0-py3.5.egg\recipy\log.py:74: in log_init
    add_git_info(run, scriptpath)
..\appdata\local\continuum\anaconda3\lib\site-packages\recipy-0.3.0-py3.5.egg\recipyCommon\version_control.py:30: in add_git_info
    repo = Repo(scriptpath, search_parent_directories=True)
..\appdata\local\continuum\anaconda3\lib\site-packages\gitpython-2.0.8-py3.5.egg\git\repo\base.py:139: in __init__
    raise NoSuchPathError(epath)
E   git.exc.NoSuchPathError: c:\Users\mjj\AppData\Local\Continuum\Anaconda3\Scripts\py.test
!!!!!!!!!!!!!!!!!!! Interrupted: 1 errors during collection !!!!!!!!!!!!!!!!!!!
=========================== 1 error in 4.55 seconds ===========================
Error in atexit._run_exitfuncs:
Traceback (most recent call last):
  File "c:\users\mjj\appdata\local\continuum\anaconda3\lib\site-packages\recipy-0.3.0-py3.5.egg\recipy\log.py", line 242, in hash_outputs
    run = db.get(eid=RUN_ID)
  File "c:\users\mjj\appdata\local\continuum\anaconda3\lib\site-packages\tinydb-3.2.1-py3.5.egg\tinydb\database.py", line 432, in get
TypeError: unhashable type: 'dict'
Error in atexit._run_exitfuncs:
Traceback (most recent call last):
  File "c:\users\mjj\appdata\local\continuum\anaconda3\lib\site-packages\recipy-0.3.0-py3.5.egg\recipy\log.py", line 231, in log_exit
    db.update({'exit_date': exit_date}, eids=[RUN_ID])
  File "c:\users\mjj\appdata\local\continuum\anaconda3\lib\site-packages\tinydb-3.2.1-py3.5.egg\tinydb\database.py", line 382, in update
  File "c:\users\mjj\appdata\local\continuum\anaconda3\lib\site-packages\tinydb-3.2.1-py3.5.egg\tinydb\database.py", line 235, in process_elements
  File "c:\users\mjj\appdata\local\continuum\anaconda3\lib\site-packages\tinydb-3.2.1-py3.5.egg\tinydb\database.py", line 381, in <lambda>
TypeError: unhashable type: 'dict'
```
