from image import Image
from transform import Transform
import mstools
import niftyreg


def register(target, moved, transform=None, interpolate=False):
    affine_template = '{0.basename}_to_{1.basename}_affine.txt'
    affine_output_filename = affine_template.format(moved, target)
    registered_image_template = '{0.basename}_aligned_to_{1.basename}.nii.gz'
    registered_image_filename = registered_image_template.format(moved, target)
    calculated_transform = None

    if transform is None:
        niftyreg.reg_aladin(
            target.filename,
            moved.filename,
            affine_output_filename,
            registered_image_filename
        )
        calculated_transform = Transform(affine_output_filename)
    else:
        if interpolate:
            interpolation_scheme = 2
        else:
            interpolation_scheme = 0
        niftyreg.reg_resample(
            target.filename,
            moved.filename,
            transform,
            registered_image_filename,
            interpolation_scheme
        )

    registered_image = Image(registered_image_filename)
    return registered_image, calculated_transform


def bias_correct(input_file):
    output_filename = '{0.basename}_biascorr'.format(input_file)
    mstools.bias_correct(input_file.filename, output_filename)
    bias_corrected_image = Image(output_filename)
    return bias_corrected_image
