from .buffered_file_data_storage import BufferedFileDataStorage
from spinn_storage_handlers.abstract_classes import \
    AbstractDataReader, AbstractContextManager
from spinn_utilities.overrides import overrides


class FileDataReader(AbstractDataReader, AbstractContextManager):
    """ A reader that can read data from a file
    """

    __slots__ = [
        # the container for the file
        "_file_container"
    ]

    def __init__(self, filename):
        """
        :param filename: The file to read
        :type filename: str
        :raise spinn_storage_handlers.exceptions.DataReadException: \
            If the file cannot found or opened for reading
        """
        self._file_container = BufferedFileDataStorage(filename, "rb")

    @overrides(AbstractDataReader.read)
    def read(self, n_bytes):
        return self._file_container.read(n_bytes)

    @overrides(AbstractDataReader.readall)
    def readall(self):
        return self._file_container.read_all()

    @overrides(AbstractDataReader.readinto)
    def readinto(self, data):
        return self._file_container.readinto(data)

    @overrides(AbstractDataReader.tell)
    def tell(self):
        return self._file_container.tell_read()

    def close(self):
        """ Closes the file

        :rtype: None
        :raise spinn_storage_handlers.exceptions.DataReadException: \
            If the file cannot be closed
        """
        self._file_container.close()
