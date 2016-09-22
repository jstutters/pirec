from collections import OrderedDict
import sys
from plumbium import call, record, pipeline
from plumbium.recorders import CSVFile


@record()
def pipeline_stage_1():
    call(['echo', 'foo'])


@record()
def pipeline_stage_2():
    call(['echo', 'data: 55'])


def my_pipeline():
    pipeline_stage_1()
    pipeline_stage_2()


def example_pipeline():
    csvfile = CSVFile(
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
