import os.path
from utils import file_sha1sum, niigz_basename


class AnalysisFile(object):
    def __init__(self, filename):
        self.filename = filename

    def checksum(self):
        return file_sha1sum(self.filename)


class Image(AnalysisFile):
    def __init__(self, filename):
        super(Image, self).__init__(filename)

    @property
    def basename(self):
        return niigz_basename(os.path.split(self.filename)[1])

    def __repr__(self):
        return 'Image({0!r})'.format(self.filename)


class Transform(AnalysisFile):
    def __init__(self, filename):
        super(Transform, self).__init__(filename)
