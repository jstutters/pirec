from collections import OrderedDict
import sys
from pirec import call, record, pipeline
from pirec.recorders import CSVFile


@record()
def pipeline_stage_1():
    call(['echo', 'foo'])


@record()
def pipeline_stage_2():
    call(['echo', 'data: 55'])


def my_pipeline():
    pipeline_stage_1()
    pipeline_stage_2()
    return 5


def example_pipeline():
    csvfile = CSVFile(
        'csv_results.csv',
        OrderedDict([
            ('subject', lambda x: x['metadata']['subject']),
            ('start_date', lambda x: x['start_date']),
            ('process_val', lambda x: x['processes'][-1]['printed_output'].strip().split(':')[1]),
            ('result_val', lambda x: x['results']['my_result'])
        ])
    )
    pipeline.run(
        'example',
        my_pipeline,
        sys.argv[1],
        metadata={'subject': 1},
        recorder=csvfile,
        result_names=('my_result',)
    )


if __name__ == '__main__':
    example_pipeline()
