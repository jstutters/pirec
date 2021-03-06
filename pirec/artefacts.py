"""Module containing the :class:`pirec.artefacts.Artefact` base class and subclasses."""

from __future__ import absolute_import
import os
import tarfile
import tempfile
from .utils import file_sha1sum


class Artefact(object):
    """Base class for Pirec artefacts (files consumed by and generated by processes).

    Args:
        filename (str): The filename of the artefact.
        extension (str): The extension of the artefact's filename.

    Keyword args:
        exists (boolean): If true raise an exception if the file does not exist.

    Raises:
        :class:`exceptions.ValueError`: If ``filename`` does not end with ``extension``.
        :class:`exceptions.IOError`: If ``filename`` does not exist.
    """

    def __init__(self, filename, extension, exists=True):
        """Initialize the artefact."""
        if not filename.endswith(extension):
            raise ValueError('Extension is not {0!r}'.format(extension))
        if exists and not os.path.exists(filename):
            raise IOError('No such file: {0!r}'.format(filename))
        self._filename = filename
        self._ext_length = len(extension)
        self._abspath = os.path.abspath(filename)

    def checksum(self):
        """Calculate the SHA-1 checksum of the file."""
        return file_sha1sum(self.filename)

    def exists(self):
        """Return ``True`` if :attr:`Artefact.filename` exists."""
        return os.path.exists(self.filename)

    @property
    def abspath(self):
        """The file's absolute path."""
        return self._abspath

    @property
    def basename(self):
        """The filename without the extension.

        .. code:: python

            >> Artefact('/dir/file.txt').basename
            '/dir/file'
        """
        return self._filename[:-self._ext_length]

    @property
    def justname(self):
        """The filename without the extension and directory components.

        .. code:: python

            >> Artefact('/dir/file.txt').justname
            'file'
        """
        return os.path.basename(self._filename)[:-self._ext_length]

    @property
    def dirname(self):
        """Return the directory component of the filename.

        .. code:: python

            >> Artefact('/dir/file.txt').dirname()
            '/dir'
        """
        return os.path.dirname(self._filename)

    def dereference(self):
        """Remove any directory components from the filename.

        .. code:: python

            >> a = Artefact('/dir/file.txt')
            >> a.dereference()
            >> a.filename
            'file.txt'
        """
        self._filename = os.path.basename(self._filename)

    @property
    def filename(self):
        """The artefact's filename."""
        return self._filename

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.filename)


class NiiGzImage(Artefact):
    """An artefact for ``.nii.gz`` images.

    Args:
        filename (str): The filename of the artefact.

    Keyword args:
        exists (boolean): If true raise an exception if the file does not exist.
    """

    extension = '.nii.gz'

    def __init__(self, filename, exists=True):
        """Initialize the artefact."""
        super(NiiGzImage, self).__init__(filename, self.extension, exists)

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.filename)


class TextFile(Artefact):
    """An artefact for ``.txt`` files.

    Args:
        filename (str): The filename of the artefact.

    Keyword args:
        exists (boolean): If true raise an exception if the file does not exist.
    """

    extension = '.txt'

    def __init__(self, filename, exists=True):
        """Initialize the artefact."""
        super(TextFile, self).__init__(filename, self.extension, exists=True)

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.filename)


def get_targz_artefact(archive_filename, filename, artefact_cls, strip_dirname=True):
    """Get an artefact from a ``.tar.gz`` file.

    Args:
        archive_name (str): The filename of the container.
        filename (str): The filename of the artefact.
        artefact_cls (Artefact): The class of the artefact.
    """
    dirname = os.path.basename(archive_filename)[0:-7]
    temp_file_handle, temp_name = tempfile.mkstemp(suffix=artefact_cls.extension)
    with tarfile.open(archive_filename, 'r:gz') as tf:
        if strip_dirname:
            member_name = os.path.join(dirname, filename)
        else:
            member_name = filename
        target_member = tf.getmember(member_name)
        extracted_file = tf.extractfile(target_member)
        with os.fdopen(temp_file_handle, 'wb') as temp_file:
            temp_file.write(extracted_file.read())
    return artefact_cls(temp_name)
