from __future__ import print_function
import datetime
from functools import wraps
import json
import os
import os.path
import shutil
from subprocess import check_output, STDOUT, CalledProcessError
import tarfile
import tempfile
import traceback


class Pipeline(object):
    def __init__(self):
        self.debug = False
        self.results = []

    def run(self, name, pipeline, base_dir, *input_files, **kwargs):
        self.results = []
        self.debug = kwargs.get('debug', False)
        self.metadata = kwargs.get('metadata', None)
        self.result_recorder = kwargs.get('recorder', None)
        self.name = name
        self.input_files = input_files
        self.base_dir = base_dir
        self.launched_dir = os.getcwd()
        self._copy_input_files_to_working_dir()
        self.start_date = datetime.datetime.now()
        os.chdir(self.working_dir)
        pipeline_exception = None
        try:
            pipeline(*input_files)
        except Exception as e:
            pipeline_exception = e
            traceback.print_exc()
        finally:
            self.finish_date = datetime.datetime.now()
            os.chdir(self.launched_dir)
            self.save(pipeline_exception)

    def _copy_input_files_to_working_dir(self):
        self.working_dir = tempfile.mkdtemp(prefix='plumbium_{0}_'.format(self.name))
        for i in self.input_files:
            dest_dir = os.path.join(self.working_dir, os.path.dirname(i.filename))
            source = os.path.join(self.base_dir, i.filename)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            shutil.copy(source, dest_dir)

    def _store_printed_output(self):
        with open('printed_output.txt', 'w') as printed_output_record:
            for r in self.results:
                printed_output_record.write(r.output)

    def record(self, result):
        self.results.append(result)

    def save(self, exception=None):
        results = {
            'name': self.name,
            'input_files': [repr(f) for f in self.input_files],
            'dir': self.base_dir,
            'start_date': self.start_date.strftime('%Y%m%d %H:%M'),
            'finish_date': self.finish_date.strftime('%Y%m%d %H:%M'),
        }
        if exception is not None:
            results['pipeline_exception'] = repr(exception)
        if self.metadata is not None:
            results['metadata'] = self.metadata
        results['processes'] = [r.as_dict() for r in self.results]
        basename = '{0}-{1}'.format(
            self.name,
            self.start_date.strftime('%Y%m%d_%H%M')
        )
        with open(os.path.join(self.working_dir, basename + '.json'), 'w') as f:
            json.dump(results, f, indent=4, separators=(',', ': '))
        archive = tarfile.open(self._clear_filename(self.base_dir, basename, '.tar.gz'), 'w:gz')
        archive.add(self.working_dir, arcname=basename)
        archive.close()
        if self.result_recorder is not None:
            self.result_recorder.write(results)

    def _clear_filename(self, directory, basename, ext):
        tgt = os.path.join(directory, basename + ext)
        if os.path.exists(tgt):
            inc = 1
            tgt = os.path.join(directory, '{0}-{1:02d}{2}'.format(basename, inc, ext))
            while os.path.exists(tgt):
                inc += 1
                tgt = os.path.join(directory, '{0}-{1:02d}{2}'.format(basename, inc, ext))
        return tgt


pipeline = Pipeline()


class OutputRecorder(object):
    def reset(self):
        self.output = ''


_output_recorder = OutputRecorder()


def call(cmd, cwd=None):
    try:
        _output_recorder.output += check_output(cmd, stderr=STDOUT, cwd=cwd)
    except CalledProcessError as e:
        print('An error occurred during: {}'.format(' '.join(cmd)))
        print('Output before failure:')
        print(e.output)
        _output_recorder.output = e.output
        raise


def record(*output_names):
    def decorator(f):
        @wraps(f)
        def process_recorder(*args, **kwargs):
            returned_images = None
            exception = None
            _output_recorder.reset()
            started = datetime.datetime.now()
            try:
                returned_images = f(*args, **kwargs)
            except:
                exception = traceback.format_exc()
                raise
            finally:
                if type(returned_images) is not tuple:
                    returned_images = (returned_images,)
                finished = datetime.datetime.now()
                named_images = dict(zip(output_names, returned_images))
                result = ProcessOutput(
                    func=f,
                    args=args,
                    kwargs=kwargs,
                    output=_output_recorder.output,
                    exception=exception,
                    started=started,
                    finished=finished,
                    **named_images
                )
                pipeline.record(result)
            return result
        return process_recorder
    return decorator


class ProcessOutput(object):
    def __init__(self, func, args, kwargs, output, exception, started, finished,  **output_images):
        self._results = output_images
        self.output = output
        self.function = func
        self.input_args = args
        self.input_kwargs = kwargs
        self.exception = exception
        self.started = started
        self.finished = finished

    def __repr__(self):
        r = self.function.__name__ + '('
        if self.input_args:
            r += ', '.join([repr(x) for x in self.input_args])
        if self.input_kwargs:
            r += ', '.join(['{0}={1!r}'.format(x) for x in self.input_kwargs])
        r += ')'
        return r

    def as_dict(self):
        d = {
            'function': self.function.__name__,
            'input_args': [repr(x) for x in self.input_args],
            'input_kwargs': {str(x[0]): repr(x[1]) for x in self.input_kwargs},
            'printed_output': self.output,
            'returned': [repr(r) for r in self._results.values()],
            'start_time': self.started.strftime('%Y%m%d %H:%M'),
            'finish_time': self.finished.strftime('%Y%m%d %H:%M')
        }
        if self.exception:
            d['exception'] = repr(self.exception)
        return d

    def __getitem__(self, key):
        return self._results[key]
