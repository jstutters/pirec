import pytest
from pirec import artefacts


def test_Artefact_basename():
    img = artefacts.Artefact('foo.nii.gz', '.nii.gz', exists=False)
    assert img.basename == 'foo'


def test_Artefact_dirname():
    img = artefacts.Artefact('dir/foo.nii.gz', '.nii.gz', exists=False)
    assert img.dirname == 'dir'
    img2 = artefacts.Artefact('/dir1/dir2/foo.nii.gz', '.nii.gz', exists=False)
    assert img2.dirname == '/dir1/dir2'
    img3 = artefacts.Artefact('foo.nii.gz', '.nii.gz', exists=False)
    assert img3.dirname == ''


def test_Artefact_basename_with_dir():
    img = artefacts.Artefact('dir/foo.nii.gz', '.nii.gz', exists=False)
    assert img.basename == 'dir/foo'


def test_Artefact_justname():
    img = artefacts.Artefact('foo.nii.gz', '.nii.gz', exists=False)
    assert img.justname == 'foo'


def test_Artefact_justname_with_dir():
    img = artefacts.Artefact('dir/foo.nii.gz', '.nii.gz', exists=False)
    assert img.justname == 'foo'


def test_Artefact_repr():
    img = artefacts.Artefact('foo.nii.gz', '.nii.gz', exists=False)
    assert repr(img) == "Artefact('foo.nii.gz')"


def test_NiiGzImage_bad_extension():
    with pytest.raises(ValueError):
        img = artefacts.NiiGzImage('foo.nii.gx', exists=False)


def test_TextFile_bad_extension():
    with pytest.raises(ValueError):
        img = artefacts.NiiGzImage('foo.txx', exists=False)


def test_exists(tmpdir):
    f = tmpdir.join('foo.txt')
    f.write('foo')
    filename = str(f)
    art = artefacts.Artefact(filename, '.txt')


def test_not_exists(tmpdir):
    f = tmpdir.join('foo.txt')
    filename = str(f)
    with pytest.raises(IOError):
        art = artefacts.Artefact(filename, '.txt')


def test_not_exists_ok(tmpdir):
    filename = str(tmpdir.join('foo.txt'))
    art = artefacts.Artefact(filename, '.txt', exists=False)
