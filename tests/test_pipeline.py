from __future__ import print_function
import os
import tarfile
import pytest
from pirec.processresult import record, pipeline, call
import pirec.artefacts as artefacts


class DummyRecorder(object):
    def write(self, results):
        self.results = results


@pytest.fixture
def simple_pipeline():
    @record('an_output')
    def recorded_function():
        call(['echo', 'test output'])
        return 'test_result'

    @record('other_output')
    def other_function(keyword_arg=123):
        call(['echo', 'other output'])

    def a_pipeline():
        recorded_function()
        other_function(keyword_arg=456)

    return a_pipeline


@pytest.fixture
def input_pipeline():
    @record('an_output')
    def recorded_function(x):
        call(['echo', str(x)])

    def a_pipeline(x):
        recorded_function(x)

    return a_pipeline


@pytest.fixture
def failing_pipeline():
    @record('an_output')
    def recorded_function():
        raise IOError

    def a_pipeline():
        recorded_function()

    return a_pipeline


@pytest.fixture
def single_return_pipeline():
    @record('an_output')
    def recorded_function():
        return 1

    def a_pipeline():
        rsl = recorded_function()
        return rsl['an_output']

    return a_pipeline


@pytest.fixture
def multiple_return_pipeline():
    @record('output1', 'output2')
    def recorded_function():
        return 1, 'a'

    def a_pipeline():
        rsl = recorded_function()
        return rsl['output1'], rsl['output2']

    return a_pipeline


@pytest.fixture
def multiple_cmd_pipeline():
    @record('an_output')
    def recorded_function(x):
        call(['echo', x])
        call(['echo', x])

    def a_pipeline():
        recorded_function('a')

    return a_pipeline


@pytest.fixture
def cat_pipeline():
    @record('cat_output')
    def recorded_function(x):
        return call(['cat', x.filename]).decode('utf-8')

    def a_pipeline(x):
        func_result = recorded_function(x)
        return (func_result['cat_output'],)

    return a_pipeline


def test_single_result(single_return_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', single_return_pipeline, str(tmpdir))
        assert pipeline.results['0'] == 1


def test_single_named_result(single_return_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', single_return_pipeline, str(tmpdir), result_names=('a_result',))
        assert pipeline.results['a_result'] == 1


def test_multiple_results(multiple_return_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', multiple_return_pipeline, str(tmpdir))
        assert pipeline.results['0'] == 1
        assert pipeline.results['1'] == 'a'


def test_multiple_named_results(multiple_return_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run(
            'test', multiple_return_pipeline, str(tmpdir),
            result_names=('result1', 'result2')
        )
        assert pipeline.results['result1'] == 1
        assert pipeline.results['result2'] == 'a'


def test_process_output(simple_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', simple_pipeline, str(tmpdir))
        assert pipeline.processes[0]['an_output'] == 'test_result'


def test_input(input_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', input_pipeline, str(tmpdir), 3)
        proc = pipeline.processes[0].as_dict()
        assert proc['printed_output'] == '3'


def test_command_captured(simple_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', simple_pipeline, str(tmpdir))
        proc = pipeline.processes[0].as_dict()
        assert proc['called_commands'] == ['echo test output']


def test_stdout_captured(simple_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', simple_pipeline, str(tmpdir))
        proc = pipeline.processes[0].as_dict()
        assert proc['printed_output'] == 'test output'


def test_exception_captured(failing_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', failing_pipeline, str(tmpdir))
        proc = pipeline.processes[0].as_dict()
        assert 'IOError' in proc['exception']


def test_kwargs_captured(simple_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', simple_pipeline, str(tmpdir))
        func_kwargs = pipeline.processes[1].as_dict()['input_kwargs']
        assert func_kwargs['keyword_arg'] == '456'


def test_multiple_commands(multiple_cmd_pipeline, tmpdir):
    with tmpdir.as_cwd():
        pipeline.run('test', multiple_cmd_pipeline, str(tmpdir))
        proc = pipeline.processes[0].as_dict()
        assert proc['called_commands'] == ['echo a', 'echo a']


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


def test_targz_artefact_pipeline(cat_pipeline, tmpdir):
    with tmpdir.as_cwd():
        with open('/tmp/foo.txt', 'w') as uncompressed_file:
            uncompressed_file.write('foo')
        tar_filename = '/tmp/foo.tar.gz'
        with tarfile.open(tar_filename, 'w:gz') as tf:
            tf.add('/tmp/foo.txt', arcname='foo/foo.txt')
        os.remove('/tmp/foo.txt')
        pipeline.run(
            'test',
            cat_pipeline,
            str(tmpdir),
            artefacts.get_targz_artefact('/tmp/foo.tar.gz', 'foo.txt', artefacts.TextFile)
        )
        print(pipeline.results)
        assert pipeline.results['0'] == 'foo'
