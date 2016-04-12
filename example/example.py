from collections import OrderedDict
import os
import sys
from plumbium import call, record, pipeline, recorders


@record()
def pipeline_stage_1():
    call([os.path.expanduser('~/programming/Plumbium/example/example_script.sh')])


@record()
def pipeline_stage_2():
    call([os.path.expanduser('~/programming/Plumbium/example/example_script2.sh')])


def my_pipeline():
    pipeline_stage_1()
    pipeline_stage_2()


def example_pipeline():
    csvfile = recorders.CSVFile(
        'csv_results.csv',
        OrderedDict([
            ('subject', lambda x: x['metadata']['subject']),
            ('start_date', lambda x: x['start_date']),
            ('data_val', lambda x: x['processes'][-1]['printed_output'].strip().split(':')[1])
        ])
    )
    pipeline.run('example', my_pipeline, sys.argv[1], metadata={'subject': 1}, recorder=csvfile)


if __name__ == '__main__':
    example_pipeline()
