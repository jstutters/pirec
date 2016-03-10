import datetime
import os.path
import shutil
from tarfile import TarFile
import tempfile


class PipelineRun(object):
    def __init__(self, pipeline, *input_files):
        self.working_dir = tempfile.mkdtemp(prefix='plumbium')
        self.pipeline = pipeline
        for i in input_files:
            shutil.copy(i.filename, self.working_dir)
            i.filename = os.path.basename(i.filename)
        self.input_files = input_files
        self.launched_dir = os.getcwd()

    def run(self):
        self.start_date = datetime.datetime.now()
        os.chdir(self.working_dir)
        try:
            self.pipeline(*self.input_files)
        finally:
            os.chdir(self.launched_dir)
            self.save()

    def save(self):
        archive_name = '{0}-{1}.tar'.format(
            self.pipeline.__name__,
            self.start_date.strftime('%Y%m%d_%H%M')
        )
        archive = TarFile(archive_name, 'w')
        archive.add(self.working_dir)
        archive.close()
