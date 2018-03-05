from spinn_storage_handlers import BufferedBytearrayDataStorage
from spinn_storage_handlers.exceptions \
    import DataWriteException, BufferedBytearrayOperationNotImplemented
import pytest
import os

testdata = bytearray(b"ABcd1234")


def test_readwrite_bytearray_buffer():
    bbds = BufferedBytearrayDataStorage()
    assert bbds is not None
    bbds.write(testdata)
    assert bbds.read_all() == testdata
    with pytest.raises(BufferedBytearrayOperationNotImplemented):
        bbds.readinto(bytearray(123))
    bbds.close()


def test_basic_ops():
    with BufferedBytearrayDataStorage() as buf:
        assert buf.tell_read() == 0
        assert buf.tell_write() == 0
        assert buf.eof() is True

        assert buf.read(123) == b''

        buf.write(bytearray(b'abc'))
        with pytest.raises(DataWriteException):
            buf.write(b'def')
        assert buf.tell_write() == 3
        assert buf.tell_read() == 0
        assert buf.eof() is False

        assert buf.read(1) == b'a'
        assert buf.tell_read() == 1
        assert buf.tell_write() == 3

        assert buf.read(5) == b'bc'
        assert buf.tell_read() == 3
        assert buf.eof() is True

        buf.seek_read(2)
        assert buf.read(5) == b'c'
        assert buf.eof() is True
        buf.write(bytearray(b'def'))
        assert buf.eof() is False
        buf.seek_read(2)
        assert buf.read(5) == b'cdef'
        assert buf.eof() is True

        buf.seek_write(2)
        buf.write(bytearray(b'PQR'))
        buf.seek_read(0)
        assert buf.read(4) == b'abPQ'
        assert buf.eof() is False

        buf.seek_write(6)
        buf.write(bytearray(b"gh"))
        buf.seek_read(1, os.SEEK_SET)
        assert buf.read(1) == b'b'
        buf.seek_read(1, os.SEEK_CUR)
        assert buf.read(1) == b'Q'
        buf.seek_read(-2, os.SEEK_END)
        assert buf.read(1) == b'g'

        with pytest.raises(IOError):
            buf.seek_read(0, "no such flag")
