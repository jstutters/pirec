import subprocess

SEG_MATHS = '/usr/local/bin/seg_maths'
SEG_STATS = '/usr/local/bin/seg_stats'
ADD = '-add'
DIV = '-div'
MUL = '-mul'
MEAN = '-a'


def seg_maths(*args):
    call = [SEG_MATHS]
    call.extend(args)
    result = subprocess.check_output(call, stderr=subprocess.STDOUT)
    return result


def seg_stats(image_filename, operation, mask_filename=None):
    call = [SEG_STATS]
    if mask_filename is not None:
        call += ['-m', mask_filename]
    call.append(operation)
    result = subprocess.check_output(call, stderr=subprocess.STDOUT)
    return result
