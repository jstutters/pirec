from processes import (
    bias_correct, register, fill_lesions, steps_brain_extraction,
    average_images, make_mtr_map, mask_image, test_process, test_failing_process
)


def fill_and_extract_brain(t1, t2, t2_lesions):
    bias_correct_output = bias_correct(t1)
    t2_register_output = register(
        bias_correct_output['bias_corrected_image'],
        t2
    )
    t2_lesions_register_output = register(
        bias_correct_output['bias_corrected_image'],
        t2_lesions,
        transform=t2_register_output['calculated_transform'],
        interpolate=False
    )
    fill_lesions_output = fill_lesions(
        bias_correct_output['bias_corrected_image'],
        t2_lesions_register_output['registered_image']
    )
    steps_output = steps_brain_extraction(
        fill_lesions_output['lesion_filled_image']
    )
    return {
        'bias_corrected_t1': bias_correct_output['bias_corrected_image'],
        'lesion_filled_t1': fill_lesions_output['lesion_filled_image'],
        'brain': steps_output['brain'],
        'brain_bin': steps_output['brain_bin']
    }


def mtr(t1, t2, t2_lesions, mton_short, mtoff_short, mton_long, mtoff_long):
    fill_and_extract_output = fill_and_extract_brain(t1, t2, t2_lesions)
    mean_mton_output = average_images(mton_short, mton_long)
    mean_mtoff_output = average_images(mtoff_short, mtoff_long)
    mtr_map_output = make_mtr_map(
        mean_mton_output['mean_image'],
        mean_mtoff_output['mean_image']
    )
    t1_registration_output = register(
        mtr_map_output['mtoff_midpoint'],
        fill_and_extract_output['bias_corrected_t1']
    )
    brain_mask_registration_output = register(
        mtr_map_output['mtoff_midpoint'],
        fill_and_extract_output['brain_bin'],
        t1_registration_output['calculated_transform'],
        interpolate=False
    )
    mask_image(
        mtr_map_output['mtr_map'],
        brain_mask_registration_output['registered_image']
    )


def test(input_file):
    test_process(input_file.filename, 'some text')


def fail_test(input_file):
    test_process(input_file.filename, 'some text')
    test_failing_process(input_file.filename, 'some text')
