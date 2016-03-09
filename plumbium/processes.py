from processresult import record_process
from image import Image
from transform import Transform
import mstools
import niftyreg
import niftyseg
import steps


@record_process('registered_image', 'calculated_transform')
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
            interpolation_scheme = niftyreg.SINC
        else:
            interpolation_scheme = niftyreg.NEAREST_NEIGHBOUR
        niftyreg.reg_resample(
            target.filename,
            moved.filename,
            transform.filename,
            registered_image_filename,
            interpolation_scheme
        )

    registered_image = Image(registered_image_filename)
    return registered_image, calculated_transform


@record_process('bias_corrected_image')
def bias_correct(input_file):
    output_filename = '{0.basename}_biascorr.nii.gz'.format(input_file)
    mstools.bias_correct(input_file.filename, output_filename)
    bias_corrected_image = Image(output_filename)
    return bias_corrected_image


@record_process('lesion_filled_image')
def fill_lesions(input_file, lesions_file):
    output_filename = '{0.basename}_lesions_filled.nii.gz'.format(input_file)
    mstools.fill_lesions(input_file.filename, lesions_file.filename, output_filename)
    return Image(output_filename)


@record_process('mean_image')
def average_images(*input_files):
    input_basenames = [i.basename for i in input_files]
    output_filename = '{0}_mean.nii.gz'.format('_'.join(input_basenames))
    operations = [input_files[0].filename]
    for i in input_files[1:]:
        operations += [niftyseg.ADD, i.filename]
    operations += [niftyseg.DIV, str(len(input_files))]
    operations.append(output_filename)
    niftyseg.seg_maths(*operations)
    return Image(output_filename)


@record_process('masked_image')
def mask_image(input_file, mask_file):
    output_filename = '{0.basename}_masked_with_{1.basename}.nii.gz'.format(
        input_file,
        mask_file
    )
    niftyseg.seg_maths(
        input_file.filename,
        niftyseg.MUL, mask_file.filename,
        output_filename
    )
    return Image(output_filename)


@record_process('brain', 'brain_bin')
def steps_brain_extraction(input_file):
    brain_filename = '{0}/{1.basename}_brain.nii.gz'.format(
        steps.OUTPUT_DIR, input_file
    )
    brain_bin_filename = '{0}/{1.basename}_brain_bin.nii.gz'.format(
        steps.OUTPUT_DIR, input_file
    )
    steps.steps(input_file.filename)
    brain_file = Image(brain_filename)
    brain_bin_file = Image(brain_bin_filename)
    return brain_file, brain_bin_file


@record_process('mtr_map', 'mtoff_midpoint', 'mton_midpoint')
def make_mtr_map(mton_file, mtoff_file):
    mtrmap_filename = 'mtrmap.nii.gz'
    mstools.mtr(mton_file.filename, mtoff_file.filename, mtrmap_filename)
    mtr_reg_tmpl = '{0}/{1.basename}_reg.nii.gz'
    mtoff_reg_filename = mtr_reg_tmpl.format(mstools.MTR_REG_DIR, mtoff_file)
    mton_reg_filename = mtr_reg_tmpl.format(mstools.MTR_REG_DIR, mton_file)
    mtrmap = Image(mtrmap_filename)
    mtoff_midpoint = Image(mtoff_reg_filename)
    mton_midpoint = Image(mton_reg_filename)
    return mtrmap, mtoff_midpoint, mton_midpoint
