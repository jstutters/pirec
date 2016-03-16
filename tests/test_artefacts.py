import pytest
from plumbium import artefacts


def test_NiiGzImage_basename():
    img = artefacts.NiiGzImage('foo.nii.gz')
    assert img.basename == 'foo'


def test_NiiGzImage_bad_extension():
    with pytest.raises(ValueError):
        img = artefacts.NiiGzImage('foo.nii.gx')
