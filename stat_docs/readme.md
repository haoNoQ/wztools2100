Stats docs
==========

Requirements
------------
  [Python 2.7](http://www.python.org/download/)
  
  [Sphinx (pip install Sphinx)](http://sphinx-doc.org/)


Compiling documentation
-----------------------
  - run `profile_to_rst.py` inside `stats/docs/`
  - run  `make.bat`  or `Makefile` inside `stat_docs/docs/`
  
  ```
  make.bat html
  ```

  - see result in build folder (`for html: html/index.html`)

Editing
-------

  - To edit sections fields edit profile/*.json
  - To edit type (contains general values) edit
  - Then adding removing sections update docs/source/index.rst manualy


Info
----
    Data outdated.
