class ProcessOutput(object):
    def __init__(self, **results):
        self.results = results

    def __getitem__(self, key):
        return self.results[key]
