from __future__ import print_function
from copy import copy
import json
import pytest
import sys
from plumbium.processresult import OutputRecorder, record, pipeline


@pytest.fixture
def recorded_pipeline():
    @record('an_output')
    def recorded_function():
        print('test output')
        return 'test_result'

    def a_pipeline():
        recorded_function()

    return a_pipeline


def test_OutputRecorder_stdout_record():
    recorder = OutputRecorder()
    with recorder.capture():
        print('test', file=sys.stdout)
    assert recorder.record == 'test\n'


def test_OutputRecorder_stderr_record():
    recorder = OutputRecorder()
    with recorder.capture():
        print('test', file=sys.stderr)
    assert recorder.record == 'test\n'


def test_OutputRecorder_releases():
    pre_test_stdout_fileno = sys.stdout.fileno()
    pre_test_stderr_fileno = sys.stderr.fileno()
    recorder = OutputRecorder()
    with recorder.capture():
        print('test', file=sys.stderr)
    sys.stdout == pre_test_stdout_fileno
    sys.stderr == pre_test_stderr_fileno


def test_Pipeline_record(recorded_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', recorded_pipeline)
        print(pipeline.results)
        assert pipeline.results[0].output == 'test output\n'
        assert pipeline.results[0]['an_output'] == 'test_result'


def test_Pipeline_save(recorded_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', recorded_pipeline)
        pipeline.save()
        json_name = '{0}-{1}.json'.format(
            pipeline.name,
            pipeline.start_date.strftime('%Y%m%d_%H%M')
        )
        with open(json_name, 'r') as op_file:
            op = json.load(op_file)
            assert op['name'] == 'test'
            proc = op['processes'][0]
            assert proc['function'] == 'recorded_function'
            assert proc['printed_output'] == 'test output\n'
