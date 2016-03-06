import pytest
from fixtures import no_subprocess
from plumbium import steps


def test_steps(no_subprocess):
    steps.steps('input.nii.gz')
    expected_call = [
        steps.STEPS_SCRIPT,
        'input.nii.gz',
        steps.OUTPUT_DIR
    ]
    assert expected_call in no_subprocess.calls
