Next steps
==========

Adding metadata
---------------

Often it is useful to add extra information to an analysis record such as
software versions or patient identification numbers.  This information can be
added to an analysis using the ``metadata`` keyword argument.

.. code:: python

    pipeline.run(
        'example',
        my_pipeline,
        base_directory,
        metadata={'site': 5, 'subject': 1, 'version': '0.1beta2'}
    )

This metadata dictionary will be included in the saved JSON file and can be
used by result recorders and to name output files.


Output file naming
------------------

By default the results of an analysis run are saved as
``'[analysis_name]-[start date]_[start_time].tar.gz'``.  This behaviour can be
changed by adding the ``filename`` keyword to your :func:`pipeline.run
<plumbium.processresult.Pipeline.run>` call.

.. code:: python

    pipeline.run(
        'example',
        my_pipeline,
        base_directory,
        metadata={'site': 5, 'subject': 1},
        filename='{name}-{metadata[site]:03d}-{metadata[subject]:02d}-{start_date:%Y%m%d}'
    )

The filename argument should be given as a string using Python's `format string
syntax <https://docs.python.org/2/library/string.html#format-string-syntax>`_.
When the file is saved the fields in this string will be replaced using the
results structure - the layout of this structure can be seen by inspecting the
JSON file that Plumbium produces.


Recording results
-----------------

In addition to archiving analysis results to a file Plumbium can record
analysis outcomes to a number of other destinations.

CSV file
++++++++

The :class:`CSVFile <plumbium.recorders.csvfile.CSVFile>` recorder outputs selected
fields from the results structure to a CSV file (which will be created or
appended to as appropriate).  To use CSVFile first create an instance of the class.

.. code:: python

    csvfile = CSVFile(
        'csv_results.csv',
        OrderedDict([
            ('start_date', lambda x: x['start_date']),
            ('data_val', lambda x: x['processes'][-1]['printed_output'].strip().split(' ')[0])
        ])
    )

The first argument is the path of the CSV file you want to record to.  The
second argument is a dictionary consisting of keys corresponding to the column
names in your CSV file and function which will return the appropriate value for
each column.  An :class:`OrderedDict <collections.OrderedDict>` should be used
so that the columns are ordered as expected (using a regular `dict` will give a
random order of columns.

SQL database
++++++++++++

To record to any SQL database supported by `SQLAlchemy
<http://www.sqlalchemy.org/>`_ use the :class:`SQLDatabase
<plumbium.recorders.sqldatabase.SQLDatabase>` class.

.. code:: python

    db = SQLDatabase(
        'sqlite:///db.sqlite',
        'results',
        {
            'wordcount': lambda x: x['processes'][-1]['printed_output'].strip().split(' ')[0],
            'start_date', lambda x: x['start_date']
        }
    )

The first argument should be a database URL in a `form recognised by SQLAlchemy
<http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html>`_, the second
argument is the name of the database table to insert the new result into (this
table must exist - Plumbium won't try to create it), the last argument is a
dictionary of column names and functions to output values as described above.

MongoDB
+++++++

Plumbium can save the complete JSON result structure to a MongoDB server using
the :class:`MongoDB <plumbium.recorders.mongodb.MongoDB>` class.

.. code:: python

    mongodb = MongoDB('mongodb://localhost:27017/', 'plumbium', 'results')

The first arugment is a MongoDB URL (see the `PyMongo tutorial
<https://api.mongodb.org/python/current/tutorial.html>`_ for details).  The
second argument is the database name and the final argument is the collection
to insert into.
