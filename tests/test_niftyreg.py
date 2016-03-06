import pytest
from fixtures import no_subprocess
from plumbium import niftyreg


def test_reg_aladin(no_subprocess):
    expected_call = [
        niftyreg.REG_ALADIN,
        '-ref', 'ref.nii.gz',
        '-flo', 'flo.nii.gz',
        '-aff', 'affine.txt',
        '-res', 'reg.nii.gz'
    ]
    reg_aladin_call = niftyreg.reg_aladin('ref.nii.gz', 'flo.nii.gz', 'affine.txt', 'reg.nii.gz')
    assert expected_call in no_subprocess.calls


def test_reg_resample(no_subprocess):
    expected_call = [
        niftyreg.REG_RESAMPLE,
        '-ref', 'ref.nii.gz',
        '-flo', 'flo.nii.gz',
        '-aff', 'affine.txt',
        '-res', 'reg.nii.gz',
        '-inter', niftyreg.SINC
    ]
    reg_resample_call = niftyreg.reg_resample('ref.nii.gz', 'flo.nii.gz', 'affine.txt', 'reg.nii.gz', '2')
    assert expected_call in no_subprocess.calls
