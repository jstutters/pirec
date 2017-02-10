from __future__ import print_function
from pirec import record


def test_recorded_func_outside_pipeline():
    @record()
    def foo():
        print('foo')

    foo()
