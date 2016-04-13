from plumbium import call, record, pipeline
from plumbium.artefacts import TextFile
import os


@record()
def pipeline_stage_1(f):
    print 'calling cat on', f.filename, 'in', os.getcwd()
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
        '/Users/jstutters/proj/Plumbium/example',
        TextFile('m0/data.txt'), TextFile('m12/data.txt')
    )


if __name__ == '__main__':
    example_pipeline()
