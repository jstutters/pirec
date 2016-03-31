import pytest
from plumbium import artefacts


def test_Artefact_basename():
    img = artefacts.Artefact('foo.nii.gz', '.nii.gz')
    assert img.basename == 'foo'


def test_Artefact_dirname():
    img = artefacts.Artefact('dir/foo.nii.gz', '.nii.gz')
    assert img.dirname == 'dir'
    img2 = artefacts.Artefact('/dir1/dir2/foo.nii.gz', '.nii.gz')
    assert img2.dirname == '/dir1/dir2'
    img3 = artefacts.Artefact('foo.nii.gz', '.nii.gz')
    assert img3.dirname == ''


def test_Artefact_basename_with_dir():
    img = artefacts.Artefact('dir/foo.nii.gz', '.nii.gz')
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
