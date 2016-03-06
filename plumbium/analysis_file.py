from checksum import file_sha1sum


class AnalysisFile(object):
    def __init__(self, filename):
        self.filename = filename

    def checksum(self):
        return file_sha1sum(self.filename)
