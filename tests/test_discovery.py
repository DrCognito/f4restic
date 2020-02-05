import f4restic.file.discovery as f4rdisco
import pathlib


def test_discovery_basic(fake_fs):
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
