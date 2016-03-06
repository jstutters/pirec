import pytest
from fixtures import no_subprocess
from plumbium import mstools, steps, niftyreg, niftyseg
from plumbium.pipelines import fill_and_extract_brain, mtr
from plumbium.image import Image

t1 = Image('t1.nii.gz')
t2 = Image('t2.nii.gz')
t2_lesions = Image('t2_lesions.nii.gz')
mtoff_short_echo = Image('mtoff_short_echo.nii.gz')
mton_short_echo = Image('mton_short_echo.nii.gz')
mtoff_long_echo = Image('mtoff_long_echo.nii.gz')
mton_long_echo = Image('mton_long_echo.nii.gz')

fill_and_extract_brain_commands = [
    mstools.BIASCORR + ' -in t1.nii.gz -out t1_biascorr.nii.gz',
    niftyreg.REG_ALADIN + ' -ref t1_biascorr.nii.gz -flo t2.nii.gz -aff t2_to_t1_biascorr_affine.txt -res t2_aligned_to_t1_biascorr.nii.gz',
    niftyreg.REG_RESAMPLE + ' -ref t1_biascorr.nii.gz -flo t2_lesions.nii.gz -aff t2_to_t1_biascorr_affine.txt -res t2_lesions_aligned_to_t1_biascorr.nii.gz -inter 0',
    mstools.NIFTK_FILL + ' -in t1_biascorr.nii.gz -lesion t2_lesions_aligned_to_t1_biascorr.nii.gz -out t1_biascorr_lesions_filled.nii.gz -input_space -dil 1 -atlas_t1 ' + mstools.NIFTK_FILL_ATLAS_T1 + ' -atlas_t2 ' + mstools.NIFTK_FILL_ATLAS_T2 + ' -atlas_mask ' + mstools.NIFTK_FILL_ATLAS_MASK,
    steps.STEPS_SCRIPT + ' t1_biascorr_lesions_filled.nii.gz ' + steps.OUTPUT_DIR,
]

mtr_commands = fill_and_extract_brain_commands + [
    niftyseg.SEG_MATHS + ' mton_short_echo.nii.gz -add mton_long_echo.nii.gz -div 2 mton_short_echo_mton_long_echo_mean.nii.gz',
    niftyseg.SEG_MATHS + ' mtoff_short_echo.nii.gz -add mtoff_long_echo.nii.gz -div 2 mtoff_short_echo_mtoff_long_echo_mean.nii.gz',
    mstools.MTR_MAP + ' -mton mton_short_echo_mton_long_echo_mean.nii.gz -mtoff mtoff_short_echo_mtoff_long_echo_mean.nii.gz -out mtrmap.nii.gz',
    niftyreg.REG_ALADIN + ' -ref MTR_map/mtoff_short_echo_mtoff_long_echo_mean_reg.nii.gz -flo t1_biascorr.nii.gz -aff t1_biascorr_to_mtoff_short_echo_mtoff_long_echo_mean_reg_affine.txt -res t1_biascorr_aligned_to_mtoff_short_echo_mtoff_long_echo_mean_reg.nii.gz',
    niftyreg.REG_RESAMPLE + ' -ref MTR_map/mtoff_short_echo_mtoff_long_echo_mean_reg.nii.gz -flo steps_output/t1_biascorr_lesions_filled_brain_bin.nii.gz -aff t1_biascorr_to_mtoff_short_echo_mtoff_long_echo_mean_reg_affine.txt -res t1_biascorr_lesions_filled_brain_bin_aligned_to_mtoff_short_echo_mtoff_long_echo_mean_reg.nii.gz -inter 0',
    niftyseg.SEG_MATHS + ' mtrmap.nii.gz -mul t1_biascorr_lesions_filled_brain_bin_aligned_to_mtoff_short_echo_mtoff_long_echo_mean_reg.nii.gz mtrmap_masked_with_t1_biascorr_lesions_filled_brain_bin_aligned_to_mtoff_short_echo_mtoff_long_echo_mean_reg.nii.gz'
]

def test_fill_lesions_and_extract_brain(no_subprocess):
    expected_calls = [cmd.split(' ') for cmd in fill_and_extract_brain_commands]
    fill_and_extract_brain(t1, t2, t2_lesions)
    assert expected_calls == no_subprocess.calls


def test_mtr(no_subprocess):
    expected_calls = [cmd.split(' ') for cmd in mtr_commands]
    mtr(t1, t2, t2_lesions, mton_short_echo, mtoff_short_echo, mton_long_echo, mtoff_long_echo)
    assert expected_calls == no_subprocess.calls

