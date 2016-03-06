import os.path
from analysis_file import AnalysisFile
from utils import niigz_basename


class Image(AnalysisFile):
    def __init__(self, filename):
        super(Image, self).__init__(filename)

    @property
    def basename(self):
        return niigz_basename(os.path.split(self.filename)[1])
