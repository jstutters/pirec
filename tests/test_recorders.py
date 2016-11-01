import pytest
from plumbium.processresult import record, pipeline, call
from plumbium.recorders import CSVFile, StdOut
from collections import OrderedDict


@pytest.fixture
def simple_pipeline():
    @record()
    def recorded_function():
        call(['echo', '6.35'])

    def a_pipeline():
        recorded_function()

    return a_pipeline


@pytest.fixture
def returning_pipeline():
    @record('value')
    def recorded_function():
        return 5.12

    def a_pipeline():
        recorded_function()

    return a_pipeline


def test_csvfile(simple_pipeline, tmpdir):
    with tmpdir.as_cwd():
        recorder = CSVFile(
            'test.csv',
            OrderedDict([
                ('id', lambda x: x['metadata']['id']),
                ('data', lambda x: x['processes'][0]['printed_output'].strip())
            ])
        )
        pipeline.run(
            'test',
            simple_pipeline,
            str(tmpdir),
            metadata={'id': 1},
            recorder=recorder
        )
        with open('test.csv') as f:
            assert f.readline().strip() == 'id,data'
            assert f.readline().strip() == '1,6.35'


def test_stdout(simple_pipeline, tmpdir, capsys):
    with tmpdir.as_cwd():
        recorder = StdOut(
            OrderedDict([
                ('id', lambda x: x['metadata']['id']),
                ('data', lambda x: x['processes'][0]['printed_output'].strip())
            ])
        )
        pipeline.run(
            'test',
            simple_pipeline,
            str(tmpdir),
            metadata={'id': 1},
            recorder=recorder
        )
    out, err = capsys.readouterr()
    assert out == 'id: 1\ndata: 6.35\n'


def test_multiple_recorders(simple_pipeline, tmpdir, capsys):
    with tmpdir.as_cwd():
        stdout1 = StdOut(
            OrderedDict([
                ('id1', lambda x: x['metadata']['id']),
                ('data1', lambda x: x['processes'][0]['printed_output'].strip())
            ])
        )
        stdout2 = StdOut(
            OrderedDict([
                ('id2', lambda x: x['metadata']['id']),
                ('data2', lambda x: x['processes'][0]['printed_output'].strip())
            ])
        )
        recorders = [stdout1, stdout2]
        pipeline.run(
            'test',
            simple_pipeline,
            str(tmpdir),
            metadata={'id': 1},
            recorder=recorders
        )
    out, err = capsys.readouterr()
    assert out == 'id1: 1\ndata1: 6.35\nid2: 1\ndata2: 6.35\n'


def test_return_record(returning_pipeline, tmpdir):
    with tmpdir.as_cwd():
        recorder = CSVFile(
            'test.csv',
            OrderedDict([
                ('data', lambda x: x['processes'][0]['returned'][0].strip())
            ])
        )
        pipeline.run(
            'test',
            returning_pipeline,
            str(tmpdir),
            metadata={'id': 1},
            recorder=recorder
        )
        with open('test.csv') as f:
            assert f.readline().strip() == 'data'
            assert f.readline().strip() == '5.12'
