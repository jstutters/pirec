from __future__ import print_function
from contextlib import contextmanager
import datetime
from functools import wraps
import json
import os.path
import shutil
from tarfile import TarFile
import tempfile
import traceback
import sys


class Pipeline(object):
    def __init__(self):
        self.debug = False
        self.results = []

    def run(self, name, pipeline, *input_files, **kwargs):
        self.results = []
        self.debug = kwargs.get('debug', False)
        self.name = name
        self.input_files = input_files
        self.launched_dir = os.getcwd()
        self._copy_input_files_to_working_dir()
        self.start_date = datetime.datetime.now()
        os.chdir(self.working_dir)
        pipeline(*input_files)
        os.chdir(self.launched_dir)
        self.save()

    def _copy_input_files_to_working_dir(self):
        self.working_dir = tempfile.mkdtemp(prefix='plumbium_{0}_'.format(self.name))
        for i in self.input_files:
            shutil.copy(i.filename, self.working_dir)
            i.filename = os.path.basename(i.filename)

    def _store_printed_output(self):
        with open('printed_output.txt', 'w') as printed_output_record:
            for r in self.results:
                printed_output_record.write(r.output)

    def record(self, result):
        self.results.append(result)

    def save(self):
        results = {
            'name': self.name,
            'input_files': [repr(f) for f in self.input_files],
            'dir': self.launched_dir,
            'start_date': self.start_date.strftime('%Y%m%d %H:%M'),
        }
        results['processes'] = [r.as_dict() for r in self.results]
        basename = '{0}-{1}'.format(
            self.name,
            self.start_date.strftime('%Y%m%d_%H%M')
        )
        with open(basename + '.json', 'w') as f:
            json.dump(results, f, indent=4, separators=(',', ': '))
        archive = TarFile(basename + '.tar', 'w')
        archive.add(self.working_dir, arcname='')
        archive.close()


pipeline = Pipeline()


class OutputRecorder(object):
    def __init__(self):
        self.record = ''

    @contextmanager
    def capture(self):
        current_stdout, current_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = self, self
        try:
            yield
        finally:
            sys.stdout, sys.stderr = current_stdout, current_stderr

    def write(self, data):
        self.record += data


def record(*output_names):
    def decorator(f):
        @wraps(f)
        def process_recorder(*args, **kwargs):
            output_rec = OutputRecorder()
            returned_images = None
            exception = None
            try:
                if not pipeline.debug:
                    with output_rec.capture():
                        returned_images = f(*args, **kwargs)
                else:
                    returned_images = f(*args, **kwargs)
            except:
                traceback.print_exc(file=sys.stderr)
                exception = traceback.format_exc()
            if type(returned_images) is not tuple:
                returned_images = (returned_images,)
            named_images = dict(zip(output_names, returned_images))
            result = ProcessOutput(
                func=f,
                args=args,
                kwargs=kwargs,
                output=output_rec.record,
                exception=exception,
                **named_images
            )
            pipeline.record(result)
            return result
        return process_recorder
    return decorator


class ProcessOutput(object):
    def __init__(self, func, args, kwargs, output, exception, **output_images):
        self._results = output_images
        self.output = output
        self.function = func
        self.input_args = args
        self.input_kwargs = kwargs
        self.exception = exception

    def __repr__(self):
        r = self.function.__name__ + '('
        if self.input_args:
            r += ', '.join([repr(x) for x in self.input_args])
        if self.input_kwargs:
            r += ', '.join(['{0}={1!r}'.format(x) for x in self.input_kwargs])
        r += ')'
        return r

    def as_dict(self):
        return {
            'function': self.function.__name__,
            'input_args': [repr(x) for x in self.input_args],
            'input_kwargs': {str(x[0]): repr(x[1]) for x in self.input_kwargs},
            'printed_output': self.output,
            'returned': [repr(r) for r in self._results.values()],
            'exception': repr(self.exception)
        }

    def __getitem__(self, key):
        return self._results[key]
