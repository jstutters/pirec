from contextlib import contextmanager
import datetime
from functools import wraps
import os.path
import shutil
from tarfile import TarFile
import tempfile
import sys


class PipelineRecord(object):
    def __init__(self):
        self.results = []

    @contextmanager
    def begin(self, name, *input_files):
        self.results = []
        self.name = name
        self.working_dir = tempfile.mkdtemp(prefix='plumbium')
        self.input_files = input_files
        for i in input_files:
            shutil.copy(i.filename, self.working_dir)
            i.filename = os.path.basename(i.filename)
        self.input_files = input_files
        self.launched_dir = os.getcwd()
        self.start_date = datetime.datetime.now()
        os.chdir(self.working_dir)
        yield
        os.chdir(self.launched_dir)
        self.save()
        for r in self.results:
            print r

    def record(self, result):
        self.results.append(result)

    def save(self):
        archive_name = '{0}-{1}.tar'.format(
            self.name,
            self.start_date.strftime('%Y%m%d_%H:%M')
        )
        archive = TarFile(archive_name, 'w')
        archive.add(self.working_dir)
        archive.close()


recorder = PipelineRecord()


class OutputRecorder(object):
    def __init__(self):
        self.record = ''

    @contextmanager
    def capture(self):
        current_stdout, current_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self, self
        yield
        sys.stdout, sys.stderr = current_stdout, current_stderr

    def write(self, data):
        self.record += data


def record_process(*output_names):
    def decorator(f):
        @wraps(f)
        def process_recorder(*args, **kwargs):
            output_recorder = OutputRecorder()
            with output_recorder.capture():
                returned_images = f(*args, **kwargs)
            if type(returned_images) is not tuple:
                returned_images = (returned_images,)
            named_images = dict(zip(output_names, returned_images))
            result = ProcessOutput(f, args, kwargs, output_recorder.record, **named_images)
            recorder.record(result)
            return result
        return process_recorder
    return decorator


class ProcessOutput(object):
    def __init__(self, function, input_args, input_kwargs, output, **output_images):
        self._results = output_images
        self.output = output
        self.function = function
        self.input_args = input_args
        self.input_kwargs = input_kwargs

    def __repr__(self):
        r = self.function.__name__ + '('
        if self.input_args:
            r += ', '.join([repr(x) for x in self.input_args])
        if self.input_kwargs:
            r += ', '.join(['{0}={1!r}'.format(x) for x in self.input_kwargs])
        r += ')'
        return r

    def __getitem__(self, key):
        return self._results[key]
