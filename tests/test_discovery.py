import f4restic.file.discovery as f4rdisco
import pathlib
import pyfakefs.pytest_plugin


def make_some_files(fs):
    fs.create_file("/var/data/xx1.txt")
    fs.create_file("/var/data/xx1/xx2.txt")
    fs.create_file("/xx1.txt")

    return fs


def test_discovery_basic(fs):
    fs = make_some_files(fs)
    directory = pathlib.Path("/")
    pattern = "xx1.txt"
    recursive = True
    files = f4rdisco.filtered_files(directory, pattern, recursive)

    # Creating a string from the pathlib object ensure it matches the os style
    # Without this it may be incorrect for pyfakefs using a unix style
    # on windows paths.
    assert str(pathlib.Path("/xx1.txt")) in files
    assert str(pathlib.Path("/var/data/xx1.txt")) in files
    assert str(pathlib.Path("/var/data/xx2.txt")) not in files
