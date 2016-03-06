import subprocess


REG_ALADIN = '/usr/local/bin/reg_aladin'
REG_RESAMPLE = '/usr/local/bin/reg_resample'
NEAREST_NEIGHBOUR = '0'
SINC = '2'


def reg_aladin(ref, flo, affine_output, registered_output):
    call = [
        REG_ALADIN,
        '-ref', ref,
        '-flo', flo,
        '-aff', affine_output,
        '-res', registered_output
    ]
    result = subprocess.check_output(call)
    return result


def reg_resample(ref, flo, transform, registered_output, interpolation_scheme):
    call = [
        REG_RESAMPLE,
        '-ref', ref,
        '-flo', flo,
        '-aff', transform,
        '-res', registered_output,
        '-inter', interpolation_scheme
    ]
    result = subprocess.check_output(call)
    return result
