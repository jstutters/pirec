import os
import subprocess

# scripts
BIASCORR = "/analysis_tools/mstools/niftkBiasFieldCorrection.py"
MTR_MAP = '/analysis_tools/mstools/niftkMTRMap.py'
NIFTK_FILL = "/analysis_tools/mstools/niftkT1PDT2Lesions.py"

# reference files
BIASCORR_MASK = "/usr/local/fsl/data/standard/MNI152_T1_2mm_brain_mask_dil.nii.gz"
BIASCORR_ATLAS = "/usr/local/fsl/data/standard/MNI152_T1_2mm.nii.gz"
NIFTK_FILL_ATLAS_T1 = '/usr/local/fsl/data/standard/MNI152_T1_1mm.nii.gz'
NIFTK_FILL_ATLAS_T2 = '/usr/local/spm12/canonical/avg152T2.nii'
NIFTK_FILL_ATLAS_MASK = '/usr/local/fsl/data/standard/MNI152_T1_1mm_brain_mask.nii.gz'

# fixed dirs
MTR_REG_DIR = 'MTR_map'


def bias_correct(input_filename, output_filename):
    call = [BIASCORR, '-in', input_filename, '-out', output_filename]
    result = subprocess.check_output(call, stderr=subprocess.STDOUT)
    return result


def fill_lesions(input_filename, lesion_filename, output_filename, dilate='1'):
    call = [
        NIFTK_FILL,
        '-in', input_filename,
        '-lesion', lesion_filename,
        '-out', output_filename,
        '-input_space',
        '-dil', dilate,
        '-atlas_t1', NIFTK_FILL_ATLAS_T1,
        '-atlas_t2', NIFTK_FILL_ATLAS_T2,
        '-atlas_mask', NIFTK_FILL_ATLAS_MASK
    ]
    result = subprocess.check_output(call, stderr=subprocess.STDOUT)
    return result


def mtr(mton_filename, mtoff_filename, mtrmap_filename):
    env = os.environ.copy()
    env['NIFTYREGDIR'] = '/opt/niftyreg-git/bin/'
    call = [
        MTR_MAP,
        '-mton', mton_filename,
        '-mtoff', mtoff_filename,
        '-out', mtrmap_filename
    ]
    result = subprocess.check_output(call, stderr=subprocess.STDOUT, env=env)
    return result
