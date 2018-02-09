import pytest
from spinn_storage_handlers.exceptions import DataReadException,\
    DataWriteException
from spinn_storage_handlers \
    import FileDataReader, FileDataWriter, BufferedFileDataStorage


testdata = bytearray("ABcd1234")


@pytest.yield_fixture
def temp_dir(tmpdir):
    # Directory for data
    thedir = tmpdir.mkdir("test_file_data")
    assert thedir.check(exists=1)

    yield thedir

    # Cleanup
    try:
        thedir.remove(ignore_errors=True)
    except Exception:
        pass
    assert thedir.check(exists=0)


def test_read_file(temp_dir):
    p = temp_dir.join("test_read_file.txt")
    p.write_binary(testdata)
    fdr = FileDataReader(str(p))

    assert fdr is not None
    assert len(fdr.readall()) == len(testdata)

    fdr.close()


def test_write_file(temp_dir):
    p = temp_dir.join("test_write_file.txt")
    fdw = FileDataWriter(str(p))

    assert str(p) == fdw.filename

    fdw.write(testdata)
    fdw.close()
    content = p.read_binary()

    assert content is not None
    assert len(content) == len(testdata)


def test_readwrite_file_buffer(temp_dir):
    p = temp_dir.join("test_readwrite_file_buffer.txt")
    assert p.check(exists=0)

    bfds = BufferedFileDataStorage(str(p), "w+b")

    assert p.check(exists=1)
    assert p.size() == 0
    assert bfds is not None
    assert bfds._file_len == 0

    bfds.write(testdata)
    bfds.read_all()  # Force flush to the OS

    assert p.size() == len(testdata)
    assert bfds._file_len == len(testdata)
    assert bfds.read_all() == testdata

    bfds.close()

    assert p.check(exists=1)


def test_no_such_file(temp_dir):
    p = temp_dir.join("test_no_such_file.txt")
    with pytest.raises(DataReadException):
        BufferedFileDataStorage(str(p), "r")


def test_readonly(temp_dir):
    p = temp_dir.join("test_readonly.txt")
    open(str(p), "w").close()
    with BufferedFileDataStorage(str(p), "r") as f:
        with pytest.raises(DataWriteException):
            f.write("foo")
        f.read(100)
        f.seek_read(0)
        b = bytearray(100)
        f.readinto(b)


def test_writeonly(temp_dir):
    p = temp_dir.join("test_writeonly.txt")
    with BufferedFileDataStorage(str(p), "w") as f:
        f.write("foo")
        with pytest.raises(IOError):
            f.read(100)
        f.seek_write(0)
        with pytest.raises(DataReadException):
            b = bytearray(100)
            f.readinto(b)
        with pytest.raises(DataWriteException):
            f.write(12345)
