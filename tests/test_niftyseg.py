import pytest
from fixtures import no_subprocess
from plumbium import niftyseg


def test_seg_maths(no_subprocess):
    inputs = [
        'a.nii.gz',
        niftyseg.ADD, 'b.nii.gz',
        niftyseg.ADD, 'c.nii.gz',
        niftyseg.DIV, '3',
        'mean.nii.gz'
    ]
    expected_call = [niftyseg.SEG_MATHS]
    expected_call.extend(inputs)
    niftyseg.seg_maths(*inputs)
    assert expected_call in no_subprocess.calls
