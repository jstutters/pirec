import os.path
import pytest
from fixtures import no_subprocess
from plumbium import processes, steps
from plumbium.image import Image
from plumbium.transform import Transform


def test_register_no_tranform(no_subprocess):
    target = Image('target.nii.gz')
    moved = Image('moved.nii.gz')
    result = processes.register(target, moved)
    assert result['registered_image'].filename == 'moved_aligned_to_target.nii.gz'
    assert result['calculated_transform'].filename == 'moved_to_target_affine.txt'


def test_register_with_tranform_no_interpolation(no_subprocess):
    target = Image('target.nii.gz')
    moved = Image('moved.nii.gz')
    transform = Transform('moved_to_target_affine.txt')
    result = processes.register(
        target, moved,
        transform=transform,
        interpolate=False
    )
    assert result['registered_image'].filename == 'moved_aligned_to_target.nii.gz'
    assert result['calculated_transform'] is None


def test_bias_correct(no_subprocess):
    targets = [
        Image('a.nii.gz'),
        Image('b.nii.gz'),
        Image('c.nii.gz')
    ]
    result = processes.average_images(*targets)
    assert result['mean_image'].filename == 'a_b_c_mean.nii.gz'


def test_steps_brain_extraction(no_subprocess):
    input_file = Image('input.nii.gz')
    result = processes.steps_brain_extraction(input_file)
    assert result['brain'].filename == os.path.join(steps.OUTPUT_DIR, 'input_brain.nii.gz')
    assert result['brain_bin'].filename == os.path.join(steps.OUTPUT_DIR, 'input_brain_bin.nii.gz')
