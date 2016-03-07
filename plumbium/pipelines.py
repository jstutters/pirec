import processes as procs


def fill_and_extract_brain(t1, t2, t2_lesions):
    t1_bias_correct = procs.bias_correct(t1)
    t2_aligned_t1, t2_to_t1_transform = procs.register(t1_bias_correct, t2)
    t2_lesions_aligned_t1, _ = procs.register(
        t1_bias_correct,
        t2_lesions,
        t2_to_t1_transform,
        interpolate=False
    )
    t1_lesion_filled = procs.fill_lesions(t1_bias_correct, t2_lesions_aligned_t1)
    brain, brain_bin = procs.steps_brain_extraction(t1_lesion_filled)
    return t1_bias_correct, t1_lesion_filled, brain, brain_bin


def mtr(t1, t2, t2_lesions, mton_short, mtoff_short, mton_long, mtoff_long):
    t1_bias_corr, _, _, brain_bin = fill_and_extract_brain(t1, t2, t2_lesions)
    mton = procs.average_images(mton_short, mton_long)
    mtoff = procs.average_images(mtoff_short, mtoff_long)
    mtrmap, mtoff_midpoint, _ = procs.make_mtr_map(mton, mtoff)
    t1_aligned_mtr, t1_to_mtr_transform = procs.register(mtoff_midpoint, t1_bias_corr)
    mask_aligned_mtr, _ = procs.register(
        mtoff_midpoint,
        brain_bin,
        t1_to_mtr_transform,
        interpolate=False
    )
    procs.mask_image(mtrmap, mask_aligned_mtr)
