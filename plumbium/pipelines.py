from processes import (
    register, fill_lesions, average_images, make_mtr_map, mask_image,
    steps_brain_extraction, bias_correct
)


def fill_and_extract_brain(t1, t2, t2_lesions):
    t1_bias_correct = bias_correct(t1)
    t2_aligned_t1, t2_to_t1_transform = register(t1_bias_correct, t2)
    t2_lesions_aligned_t1, _ = register(
        t1_bias_correct,
        t2_lesions,
        t2_to_t1_transform,
        interpolate=False
    )
    t1_lesion_filled = fill_lesions(t1_bias_correct, t2_lesions_aligned_t1)
    brain, brain_bin = steps_brain_extraction(t1_lesion_filled)
    return t1_bias_correct, t1_lesion_filled, brain, brain_bin


def mtr(t1, t2, t2_lesions, mton_short, mtoff_short, mton_long, mtoff_long):
    t1_bias_corr, _, _, brain_bin = fill_and_extract_brain(t1, t2, t2_lesions)
    mton = average_images(mton_short, mton_long)
    mtoff = average_images(mtoff_short, mtoff_long)
    mtrmap, mtoff_midpoint, _ = make_mtr_map(mton, mtoff)
    t1_aligned_mtr, t1_to_mtr_transform = register(mtoff_midpoint, t1_bias_corr)
    mask_aligned_mtr, _ = register(
        mtoff_midpoint,
        brain_bin,
        t1_to_mtr_transform,
        interpolate=False
    )
    mask_image(mtrmap, mask_aligned_mtr)
