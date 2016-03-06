import subprocess

SEG_MATHS = '/usr/local/bin/seg_maths'
ADD = '-add'
DIV = '-div'
MUL = '-mul'


def seg_maths(*args):
    call = [SEG_MATHS]
    call.extend(args)
    result = subprocess.check_output(call, stderr=subprocess.STDOUT)
    return result
