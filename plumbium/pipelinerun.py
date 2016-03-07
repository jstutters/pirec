import gzip
import os.path
import shutil
import tarfile
import tempfile


class PipelineRun(object):
    def __init__(self, pipeline, *input_files):
        self.launched_dir = os.getcwd()
        self.working_dir = tempfile.mkdtemp(prefix='plumbium')
        for i in input_files:
            shutil.copy(i.filename, working_dir)
            i.filename = os.path.basename(i.filename)

    def run():
        self.start_date = datetime.datetime.now()
        os.chdir(self.working_dir)
        try:
            pipeline(*input_files)
        finally:
            os.chdir(launched_dir)
            self.save()

    def save():
        archive_name = '{0}-{1}.tar'.format(
            pipeline.__name__,
            start_date.strftime('%Y%m%d_%H:%M')
        )
        archive = TarFile(archive_name, 'w')
        archive.add(self.working_dir)
        archive.close()
