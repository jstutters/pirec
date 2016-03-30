from plumbium import call, record, pipeline


@record()
def pipeline_stage_1():
    call(['/Users/jstutters/proj/Plumbium/example/example_script.sh'])


@record()
def pipeline_stage_2():
    call(['/Users/jstutters/proj/Plumbium/example/example_script2.sh'])


def my_pipeline():
    pipeline_stage_1()
    pipeline_stage_2()


def example_pipeline():
    pipeline.run('example', my_pipeline)


if __name__ == '__main__':
    example_pipeline()
