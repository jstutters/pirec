import pytest
from pirec import artefacts


def test_Artefact_basename():
    """basename() should strip the extension from an artefact filename."""
    img = artefacts.Artefact('foo.nii.gz', '.nii.gz', exists=False)
    assert img.basename == 'foo'


def test_Artefact_dirname():
    """dirname() should return the path components up to the filename."""
    img = artefacts.Artefact('dir/foo.nii.gz', '.nii.gz', exists=False)
    assert img.dirname == 'dir'
    img2 = artefacts.Artefact('/dir1/dir2/foo.nii.gz', '.nii.gz', exists=False)
    assert img2.dirname == '/dir1/dir2'
    img3 = artefacts.Artefact('foo.nii.gz', '.nii.gz', exists=False)
    assert img3.dirname == ''


def test_Artefact_basename_with_dir():
    """basename() should still work in a subdirectory."""
    img = artefacts.Artefact('dir/foo.nii.gz', '.nii.gz', exists=False)
    assert img.basename == 'dir/foo'


def test_Artefact_justname():
    """justname() should work like basename() with no directory components."""
    img = artefacts.Artefact('foo.nii.gz', '.nii.gz', exists=False)
    assert img.justname == 'foo'


def test_Artefact_justname_with_dir():
    """justname() should strip extension and directory components."""
    img = artefacts.Artefact('dir/foo.nii.gz', '.nii.gz', exists=False)
    assert img.justname == 'foo'


def test_Artefact_repr():
    """Make sure __repr__() looks correct."""
    img = artefacts.Artefact('foo.nii.gz', '.nii.gz', exists=False)
    assert repr(img) == "Artefact('foo.nii.gz')"


def test_NiiGzImage_bad_extension():
    """__init__() should raise a ValueError if filename doesn't have the expected extension."""
    with pytest.raises(ValueError):
        img = artefacts.NiiGzImage('foo.nii.gx', exists=False)


def test_TextFile_bad_extension():
    with pytest.raises(ValueError):
        img = artefacts.NiiGzImage('foo.txx', exists=False)


def test_exists(tmpdir):
    """If the file is present and exists=True __init__ should work."""
    f = tmpdir.join('foo.txt')
    f.write('foo')
    filename = str(f)
    art = artefacts.Artefact(filename, '.txt')


def test_not_exists(tmpdir):
    """If the file is not present and exists=True __init__ should raise IOError."""
    f = tmpdir.join('foo.txt')
    filename = str(f)
    with pytest.raises(IOError):
        art = artefacts.Artefact(filename, '.txt')


def test_not_exists_ok(tmpdir):
    """If the file is not present and exists=False __init__ should work."""
    filename = str(tmpdir.join('foo.txt'))
    art = artefacts.Artefact(filename, '.txt', exists=False)
