.. Plumbium documentation master file, created by
   sphinx-quickstart on Tue Apr 12 21:27:58 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Plumbium's documentation!
####################################

Plumbium is a Python package for wrapping scripts so that their inputs and
outputs are preserved in a consistent way and results are recorded.


Why?
====

Does your directory listing look like this?

.. code::

    jstutters@dirac ~/my_study % ll *
    -rw-rw-r--. 1 jstutters staff 0 Apr 15 10:31 bad_results.txt
    -rw-rw-r--. 1 jstutters staff 0 Apr 15 10:32 old_method.xls
    -rw-rw-r--. 1 jstutters staff 0 Apr 15 10:31 results.txt
    -rw-rw-r--. 1 jstutters staff 0 Apr 15 10:31 use_this.data.csv

    01:
    total 8.0K
    drwxrwxr-x. 2 jstutters staff 2 Apr 15 10:34 001
    drwxrwxr-x. 2 jstutters staff 2 Apr 15 10:34 001-dont_use
    drwxrwxr-x. 2 jstutters staff 2 Apr 15 10:34 002
    drwxrwxr-x. 2 jstutters staff 2 Apr 15 10:34 002-good
    drwxrwxr-x. 2 jstutters staff 2 Apr 15 10:34 003
    -rw-rw-r--. 1 jstutters staff 0 Apr 15 10:36 subject1_t1_dont_change.nii.gz


When an analysis is run with Plumbium all the input files are copied to a
temporary directory in which the analysis is run.  When the analysis has
finished all the files created are collected into an archive and saved along
with all the printed outputs from the analysis stages and any exceptions that
occurred.  Plumbium can also record results to a database or spreadsheet.  To
find out more, read the :doc:`tutorial <tutorial>` or dive into the :ref:`API
documentation <modindex>`.


Example
-------

.. code:: python

    from plumbium import call, record, pipeline
    from plumbium.artefacts import TextFile


    @record()
    def pipeline_stage_1(f):
        call(['/bin/cat', f.filename])


    @record()
    def pipeline_stage_2(f):
        call(['/bin/cat', f.filename])


    def my_pipeline(file1, file2):
        pipeline_stage_1(file1)
        pipeline_stage_2(file2)


    def example_pipeline():
        pipeline.run(
            'example',
            my_pipeline,
            '/my/data/directory',
            TextFile('month00/data.txt'), TextFile('month12/data.txt')
        )


    if __name__ == '__main__':
        example_pipeline()


Learn more
==========

.. toctree::
   :maxdepth: 3

   installation
   tutorial
   next_steps
   contribute
   support
   modules


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

