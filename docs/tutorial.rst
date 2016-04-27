Tutorial
========

Imports
-------

To use Plumbium you should start by importing the :func:`call
<plumbium.processresult.call>` function, :func:`record <plumbium.processresult.record>`
decorator, :class:`pipeline <plumbium.processresult.Pipeline>` instance and 
any :mod:`plumbium.artefacts` you need.  Artefacts are classes representing the
data files used by your pipeline e.g. text files and images.

.. code:: python

    from plumbium import call, record, pipeline
    from plumbium.artefacts import TextFile


Processing stages
-----------------

Next, define the stages of your analysis to be recorded.  For this example
we'll concatenate two files in the first stage and then count the words of the
resulting file in the second stage.  The :func:`record
<plumbium.processresult.record>` decorator indicates that the function should
be recorded.  The list of arguments to record is used to name the return values
from the function - the number of arguments to record should match the number
of variables returned the the function.  Calls to external programs should be
made using :func:`call <plumbium.processresult.call>` so that printed output
can be captured.

.. code:: python

    @record('concatenated_file')
    def concatenate(input_1, input_2):
        cmd = 'cat {0.filename} {1.filename} > joined.txt'.format(
            input_1, input_2
        )
        call([cmd], shell=True)
        return TextFile('joined.txt')

    @record()
    def count_words(target):
        call(['wc', target.filename])



The complete pipeline
---------------------

Now to use our stages to define the whole pipeline.  Functions decorated with
:func:`record <plumbium.processresult.record>` return an instance of
:class:`ProcessOutput <plumbium.processresult.ProcessOutput>`, the outputs from
the function can be accessed using a dict-like method.

.. code:: python

    def cat_and_count(input_1, input_2):
        concatenate_output = concatenate(input_1, input_2)
        count_words(concatenate_output['concatenated_file'])


Running the pipeline
--------------------

Finally we use :func:`pipeline.run <plumbium.processresult.Pipeline.run>` to
execute the pipeline.

.. code:: python

    import sys

    if __name__ == '__main__':
        input_1 = TextFile(sys.argv[1])
        input_2 = TextFile(sys.argv[2])
        pipeline.run('cat_and_count', cat_and_count, '.', input_1, input_2)


To try this out save the complete example as tutorial.py, create a pair of text
files in the same directory and then run ``python tutorial.py [text file 1]
[text file 2]``.  If everything works no errors should be printed and a file
called ``cat_and_count-[date]_[time].tar.gz`` should be created.


Results
-------

Extract the result file using ``tar -zxf [result file]`` and have a look in the
new directory.  You'll find the two files that you used as input to the script,
the result output of concatenating the files as ``joined.txt`` and a ``.json``
file.  If you open the ``.json`` file you'll see a full record of the commands
run (any errors that occur will also be recorded in this file).

.. code:: js

    {
        "processes": [
            {
                "function": "concatenate",
                "returned": [
                    "TextFile('joined.txt')"
                ],
                "input_kwargs": {},
                "finish_time": "20160426 12:13",
                "start_time": "20160426 12:13",
                "printed_output": "",
                "input_args": [
                    "TextFile('text_file.txt')",
                    "TextFile('text_file2.txt')"
                ]
            },
            {
                "function": "count_words",
                "returned": [],
                "input_kwargs": {},
                "finish_time": "20160426 12:13",
                "start_time": "20160426 12:13",
                "printed_output": "4 joined.txt\n",
                "input_args": [
                    "TextFile('joined.txt')"
                ]
            }
        ],
        "name": "cat_and_count",
        "finish_date": "20160426 12:13",
        "start_date": "20160426 12:13",
        "dir": ".",
        "input_files": [
            "TextFile('text_file.txt')",
            "TextFile('text_file2.txt')"
        ]
    }
