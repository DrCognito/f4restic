import pytest
import pyfakefs.pytest_plugin


file_list = [
    "/var/data/xx1.txt",
    "/var/data/xx1/xx2.txt",
    "/xx1.txt",
    "/var/file1",
    "/var/file2.t",
    "/var/file3.tx",
    "/var/file4.txt",
    "/directory1/.hidden",
    "/.hidden",
    "/emptydir/",
    "/dir1/foo/dir2/bar/file",
    "/foo/bar/file",
    "/tmp/foo/bar",
]


@pytest.fixture()
def fake_fs(fs):
    for f in file_list:
        fs.create_file(f)

    yield fs
