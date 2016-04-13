.. Plumbium documentation master file, created by
   sphinx-quickstart on Tue Apr 12 21:27:58 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Plumbium's documentation!
====================================

Plumbium is a Python package for wrapping scripts so that their inputs and
outputs are preserved in a consistent way.

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

.. toctree::
   :maxdepth: 2

   installation
   contribute
   support
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

