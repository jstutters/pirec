import pytest
from fixtures import no_subprocess
from plumbium import processes
from plumbium.image import Image
from plumbium.transform import Transform


def test_register_no_tranform(no_subprocess):
    target = Image('target.nii.gz')
    moved = Image('moved.nii.gz')
    registered_image, transform = processes.register(target, moved)
    assert registered_image.filename == 'moved_aligned_to_target.nii.gz'
    assert transform.filename == 'moved_to_target_affine.txt'


def test_register_with_tranform_no_interpolation(no_subprocess):
    target = Image('target.nii.gz')
    moved = Image('moved.nii.gz')
    transform = Transform('moved_to_target_affine.txt')
    registered_image, transform = processes.register(
        target, moved,
        transform=transform,
        interpolate=False
    )
    assert registered_image.filename == 'moved_aligned_to_target.nii.gz'
    assert transform is None
