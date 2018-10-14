
Database Schema
===============

.. list-table::
   :header-rows: 1

   * - Field
     - Description
     - Example
   * - ``unique_id``
     - 
     - ff129fee-c0d9-47cc-b0a9-997a530230a8
   * - ``author``
     - Username of the one running the script
     - 
   * - ``description``
     - Currently not used?
     - 
   * - ``inputs``
     - List of input files (can be empty)
     - 
   * - ``outputs``
     - List of output files (can be empty)
     - 
   * - ``script``
     - Path to the script that was run
     - 
   * - ``command``
     - Path to the python executable that was used to run the script
     - ``/usr/bin/python2.7``
   * - ``environment``
     - Information about the environment in which the script was run (including Python version)
     - Linux-4.15.0-29-generic-x86_64-with-debian-stretch-sid python 2.7.15 -Anaconda, Inc.- (default, May 1 2018, 23:32:55)
   * - ``date``
     - Date and time the script was run (in UTC)
     - 
   * - ``command_args``
     - Command line arguments of the script (can be empty)
     - 
   * - ``warnings``
     - Warnings issued during execution of the script (if any)
     - 
   * - ``exception``
     - Exception raised during execution of the script (if any)
     - 
   * - ``libraries``
     - Names and versions of patched libraries used in this script
     - 
   * - ``notes``
     - Notes added by the user by running ``recipy annotate`` or in the gui
     - 
   * - ``custom_values``
     - Values logged explicitly in the script by calling ``recipy.log_values({'name': 'value'})``
     - 
   * - ``gitrepo``\ /\ ``svnrepo``
     - 
     - 
   * - ``gitcommit``\ /\ ``svncommit``
     - Current git/svn commit
     - 
   * - ``gitorigin``
     - 
     - 
   * - ``diff``
     - 
     - 

