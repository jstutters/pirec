import os.path
import subprocess

STEPS_SCRIPT = '/analysis_tools/steps/steps.sh'
OUTPUT_DIR = 'steps_output'


def steps(input_filename):
    call = [
        STEPS_SCRIPT,
        os.path.abspath(input_filename),
        OUTPUT_DIR
    ]
    result = subprocess.check_output(call, stderr=subprocess.STDOUT)
    return result
