import pytest
from plumbium import artefacts


def test_Artefact_basename():
    img = artefacts.Artefact('foo.nii.gz', '.nii.gz')
    assert img.basename == 'foo'


def test_Artefact_repr():
    img = artefacts.Artefact('foo.nii.gz', '.nii.gz')
    assert repr(img) == "Artefact('foo.nii.gz')"


def test_NiiGzImage_bad_extension():
    with pytest.raises(ValueError):
        img = artefacts.NiiGzImage('foo.nii.gx')


def test_TextFile_bad_extension():
    with pytest.raises(ValueError):
        img = artefacts.NiiGzImage('foo.txx')
