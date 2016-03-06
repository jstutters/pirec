import subprocess

STEPS_SCRIPT = '/analysis_tools/steps/do_steps.sh'
OUTPUT_DIR = 'steps_output'


def steps(input_filename):
    call = [
        STEPS_SCRIPT,
        input_filename,
        OUTPUT_DIR
    ]
    result = subprocess.check_output(call, stderr=subprocess.STDOUT)
    return result
