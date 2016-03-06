import pytest
from plumbium import utils


def test_niigz_basename():
    assert utils.niigz_basename('foo.nii.gz') == 'foo'


def test_niigz_basename_bad_extension():
    with pytest.raises(ValueError):
        utils.niigz_basename('foo.txt')


def test_file_sha1sum(tmpdir):
    test_file = tmpdir.join('test.txt')
    test_file.write('some test text')
    assert utils.file_sha1sum(str(test_file)) == 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
