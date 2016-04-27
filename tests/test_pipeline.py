from __future__ import print_function
import pytest
from plumbium.processresult import record, pipeline, call


class DummyRecorder(object):
    def write(self, results):
        self.results = results


@pytest.fixture
def simple_pipeline():
    @record('an_output')
    def recorded_function():
        call(['echo', 'test output'])
        return 'test_result'

    def a_pipeline():
        recorded_function()

    return a_pipeline


@pytest.fixture
def failing_pipeline():
    @record('an_output')
    def recorded_function():
        raise IOError

    def a_pipeline():
        recorded_function()

    return a_pipeline


def test_result(simple_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', simple_pipeline, str(tmpdir))
        print(pipeline.results)
        assert pipeline.results[0]['an_output'] == 'test_result'


def test_stdout_captured(simple_pipeline, tmpdir):
    with tmpdir.as_cwd():
        recorder = DummyRecorder()
        pipeline.run('test', simple_pipeline, str(tmpdir), recorder=recorder)
        proc = pipeline.results[0].as_dict()
        assert proc['printed_output'] == 'test output\n'


def test_exception_captured(failing_pipeline, tmpdir):
    with tmpdir.as_cwd():
        recorder = DummyRecorder()
        pipeline.run('test', failing_pipeline, str(tmpdir), recorder=recorder)
        proc = pipeline.results[0].as_dict()
        assert 'IOError' in proc['exception']


def test_save_filename(simple_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run(
            'test',
            simple_pipeline,
            str(tmpdir),
            metadata={'test': 1},
            filename='result_file_{metadata[test]:03d}'
        )
        assert 'result_file_001.tar.gz' in [f.basename for f in tmpdir.listdir()]
