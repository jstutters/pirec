import niftyseg


def image_mean(image, mask):
    mean_value = niftyseg.seg_stats(
        image.filename,
        niftyseg.MEAN,
        mask_filename=mask.filename
    )
    return float(mean_value)
