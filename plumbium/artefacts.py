import os.path
from utils import file_sha1sum


class Artefact(object):
    def __init__(self, filename, extension):
        if not filename.endswith(extension):
            raise ValueError
        self._filename = filename
        self._ext_length = len(extension)
        self._abspath = os.path.abspath(filename)

    def checksum(self):
        return file_sha1sum(self.filename)

    def exists(self):
        return os.path.exists(self.filename)

    @property
    def abspath(self):
        return self._abspath

    @property
    def basename(self):
        """Return the filename without the extension"""
        return self._filename[:-self._ext_length]

    def dereference(self):
        self._filename = os.path.basename(self._filename)

    @property
    def filename(self):
        return self._filename

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.filename)


class NiiGzImage(Artefact):
    def __init__(self, filename):
        super(NiiGzImage, self).__init__(filename, '.nii.gz')

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.filename)


class TextFile(Artefact):
    def __init__(self, filename):
        super(TextFile, self).__init__(filename, '.txt')

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.filename)
