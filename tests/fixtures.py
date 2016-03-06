import pytest


class CallRecorder(object):
    def __init__(self):
        self.calls = []

    def dummy_check_output(self, call, *args, **kwargs):
        self.calls.append(call)


@pytest.fixture()
def no_subprocess(monkeypatch):
    recorder = CallRecorder()
    monkeypatch.setattr('subprocess.check_output', recorder.dummy_check_output)
    return recorder
