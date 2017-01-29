Tutorial
********

Imports
-------

To use Pirec you should start by importing the :func:`call
<pirec.processresult.call>` function, :func:`record <pirec.processresult.record>`
decorator, :class:`pipeline <pirec.processresult.Pipeline>` instance and 
any :mod:`pirec.artefacts` you need.  Artefacts are classes representing the
data files used by your pipeline e.g. text files and images.

.. code:: python

    from pirec import call, record, pipeline
    from pirec.artefacts import TextFile


Processing stages
-----------------

Next, define the stages of your analysis to be recorded.  For this example
we'll concatenate two files in the first stage and then count the words of the
resulting file in the second stage.  The :func:`record
<pirec.processresult.record>` decorator indicates that the function should
be recorded.  The list of arguments to record is used to name the return values
from the function - the number of arguments to record should match the number
of variables returned the the function.  Calls to external programs should be
made using :func:`call <pirec.processresult.call>` so that printed output
can be captured.

.. code:: python

    @record('concatenated_file')
    def concatenate(input_1, input_2):
        cmd = 'cat {0.filename} {1.filename} > joined.txt'.format(
            input_1, input_2
        )
        call([cmd], shell=True)
        return TextFile('joined.txt')

    @record(count)
    def count_words(target):
        wc_output = call(['wc', target.filename])
        return int(wc_output.strip())



The complete pipeline
---------------------

Now to use our stages to define the whole pipeline.  Functions decorated with
:func:`record <pirec.processresult.record>` return an instance of
:class:`ProcessOutput <pirec.processresult.ProcessOutput>`, the outputs from
the function can be accessed using a dict-like method.

.. code:: python

    def cat_and_count(input_1, input_2):
        concatenate_output = concatenate(input_1, input_2)
        count_output = count_words(concatenate_output['concatenated_file'])
        return count_output['count']


Running the pipeline
--------------------

Finally we use :func:`pipeline.run <pirec.processresult.Pipeline.run>` to
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
                ],
                "called_commands": [
                    "cat text_file.txt text_file2.txt"
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
                ],
                "called_commands": [
                    "wc joined.txt"
                ]
            }
        ],
        "name": "cat_and_count",
        "finish_date": "20160426 12:13",
        "start_date": "20160426 12:13",
        "results": {
            "0": 1234
        },
        "dir": ".",
        "inputs: [
            "TextFile('text_file.txt')",
            "TextFile('text_file2.txt')"
        ],
        "environment": {
            "python_packages": [
                ...
            ],
            "hostname": "machine.example.com",
            "environ": {
                ...
            },
            "uname": [
                "Linux"
                "machine.example.com"
                "3.10.0-327.18.2.el7.x86_64",
                "#1 SMP Thu May 12 11:03:55 UTC 2016",
                "x86_64"
            ]
        }
    }
