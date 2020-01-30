import pyfakefs.pytest_plugin
import os
import pathlib


def test_makefs_makefile(fs):
    # "fs" is the reference to the fake file system
    fs.create_file("/var/data/xx1.txt")
    assert os.path.exists("/var/data/xx1.txt")


def test_makefs_pathlib(fs):
    fs.create_file("/var/data/xx1.txt")
    test = pathlib.Path('/var/data/xx1.txt')
    assert test.exists()
