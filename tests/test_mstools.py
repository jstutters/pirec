import pytest
from fixtures import no_subprocess
from plumbium import mstools


def test_bias_correct(no_subprocess):
    input_filename = 'input.nii.gz'
    output_filename = 'output.nii.gz'
    expected_call = [
        mstools.BIASCORR,
        '-in', input_filename,
        '-out', output_filename
    ]
    mstools.bias_correct(input_filename, output_filename)
    assert expected_call in no_subprocess.calls


def test_fill_lesions(no_subprocess):
    input_filename = 'input.nii.gz'
    lesion_filename = 'lesions.nii.gz'
    output_filename = 'output.nii.gz'
    expected_call = [
        mstools.NIFTK_FILL,
        '-in', input_filename,
        '-lesion', lesion_filename,
        '-out', output_filename,
        '-input_space',
        '-dil', '1',
        '-atlas_t1', mstools.NIFTK_FILL_ATLAS_T1,
        '-atlas_t2', mstools.NIFTK_FILL_ATLAS_T2,
        '-atlas_mask', mstools.NIFTK_FILL_ATLAS_MASK
    ]
    mstools.fill_lesions(input_filename, lesion_filename, output_filename)
    assert expected_call in no_subprocess.calls
