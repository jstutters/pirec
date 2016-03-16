import os.path
from utils import file_sha1sum


class Artefact(object):
    def __init__(self, filename, extension):
        if not filename.endswith(extension):
            raise ValueError
        self.filename = filename
        self._ext_length = len(extension)

    def checksum(self):
        return file_sha1sum(self.filename)

    @property
    def basename(self):
        """Return the filename without the extension"""
        return self.filename[:-self._ext_length]

    def __repr__(self):
        return 'Artefact({0!r})'.format(self.filename)


class NiiGzImage(Artefact):
    def __init__(self, filename):
        super(NiiGzImage, self).__init__(filename, '.nii.gz')


    def __repr__(self):
        return '{0}({1!r})'.format(self.__clsname__, self.filename)


class TextFile(Artefact):
    def __init__(self, filename):
        super(TextFile, self).__init__(filename, '.txt')

    def __repr__(self):
        return '{0}({1!r})'.format(self.__clsname__, self.filename)
