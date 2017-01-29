from pirec import utils


def test_file_sha1sum(tmpdir):
    test_file = tmpdir.join('test.txt')
    test_file.write('some test text')
    assert utils.file_sha1sum(str(test_file)) == '765fd0fb4ae6bc524d60acf1eedd2e7fd870d0c7'
