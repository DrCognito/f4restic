import f4restic.file.filegroup as f4rgroup
import pathlib
import typing as typ
import fnmatch
import pytest


def test_filegroup_filter_basic1():
    pair1 = (pathlib.Path("/fake/text.txt"), "*text", False)
    pair2 = (pathlib.Path("/fake/text.txt"), "*text", True)

    test_group = f4rgroup.FileGroup(includes={pair1,})

    assert pair1 in test_group.includes

    test_group.includes.add(pair2)

    assert pair2 in test_group.includes


def test_filegroup_filter_basic2(fake_fs):
    pair2 = (pathlib.Path("/fake/text.txt"), "*text", True)

    test_group = f4rgroup.FileGroup()
    test_group.includes.add(pair2)
    assert pair2 in test_group.includes


def test_filegroup_include_empty():

    test_group = f4rgroup.FileGroup()
    assert isinstance(test_group.get_file_list(), typ.Set)


def test_filegroup_include_real():
    # Should be the base directory of this module
    single = (pathlib.Path("./"), "*", False)
    test_group = f4rgroup.FileGroup(includes={single,})
    file_list = test_group.get_file_list()

    assert isinstance(file_list, typ.Set)
    assert len(file_list) > 0


def test_filegroup_include_recurse():
    none_rec_py = (pathlib.Path("./"), "*.py", False)
    test_nr = f4rgroup.FileGroup(includes={none_rec_py,})

    rec_py = (pathlib.Path("./"), "*.py", True)
    test_rec = f4rgroup.FileGroup(includes={rec_py,})

    nr_list = test_nr.get_file_list()
    rec_list = test_rec.get_file_list()

    assert len(rec_list) > len(nr_list)
    assert set(nr_list).issubset(rec_list)


def test_filegroup_include_file(fake_fs):
    # single file
    single = (pathlib.Path("/var/data/"), "*.txt", True)
    test_group = f4rgroup.FileGroup(includes={single,})
    assert str(pathlib.Path("/var/data/xx1.txt")) in test_group.get_file_list()
    assert str(pathlib.Path("/var/data/xx1/xx2.txt")) in test_group.get_file_list()


def test_filegroup_include_directory_rec(fake_fs):
    # directory
    directory = (pathlib.Path("/var/data/"), "*.txt", True)
    test_group = f4rgroup.FileGroup(includes={directory,})
    assert str(pathlib.Path("/var/data/xx1.txt")) in test_group.get_file_list()
    assert str(pathlib.Path("/var/data/xx1/xx2.txt")) in test_group.get_file_list()


def test_filegroup_include_directory(fake_fs):
    # directory
    directory = (pathlib.Path("/var/data/"), "*", False)
    test_group = f4rgroup.FileGroup(includes={directory,})
    assert str(pathlib.Path("/var/data/xx1.txt")) in test_group.get_file_list()
    assert str(pathlib.Path("/var/data/xx1/xx2.txt")) not in test_group.get_file_list()


def test_filegroup_include_empty_directory(fake_fs):
    # emptydir
    empty_directory = (pathlib.Path("/"), "*emptydir*", True)
    test_group = f4rgroup.FileGroup(includes={empty_directory,})
    assert str(pathlib.Path("/emptydir/")) in test_group.get_file_list()


def test_filegroup_include_hidden1(fake_fs):
    # hidden
    hidden = (pathlib.Path("/"), ".*", False)
    test_group = f4rgroup.FileGroup(includes={hidden,})
    assert str(pathlib.Path("/.hidden")) in test_group.get_file_list()


def test_filegroup_include_hidden2(fake_fs):
    hidden_sub = (pathlib.Path("/directory1/"), ".*", True)
    test_group = f4rgroup.FileGroup(includes={hidden_sub,})
    assert str(pathlib.Path("/directory1/.hidden")) in test_group.get_file_list()


def test_filegroup_include_2filt(fake_fs):
    filt1 = (pathlib.Path("/var/"), "*.t", True)
    filt2 = (pathlib.Path("/var/"), "*.tx", True)

    test_group = f4rgroup.FileGroup(includes={filt1, filt2})
    files = test_group.get_file_list()

    assert str(pathlib.Path("/var/file1")) not in files
    assert str(pathlib.Path("/var/file2.t")) in files
    assert str(pathlib.Path("/var/file3.tx")) in files
    assert str(pathlib.Path("/var/file4.txt")) not in files


def test_special_wildcard(fake_fs):
    filt1 = (pathlib.Path("/"), "foo/**/bar", True)

    test_group = f4rgroup.FileGroup(includes={filt1,})
    files = test_group.get_file_list()
    print(files)

    assert str(pathlib.Path("/dir1/foo/dir2/bar/file")) in files
    assert str(pathlib.Path("/foo/bar/file")) in files
    assert str(pathlib.Path("/tmp/foo/bar")) in files


def test_filegroup_exclude_all(fake_fs):
    filt1 = (pathlib.Path("/"), "*.t", True)
    filt2 = (pathlib.Path("/arr/"), "*.txt", False)

    test_group = f4rgroup.FileGroup(excludes={filt1,})

    assert filt1 in test_group.excludes

    test_group.excludes.add(filt2)

    assert filt2 in test_group.excludes


def test_filegroup_exclude_txt(fake_fs):
    file_match = "*.txt"
    filt1 = (pathlib.Path("/"), "*", True)
    filt2 = (pathlib.Path("/"), file_match, True)

    test_group = f4rgroup.FileGroup(includes={filt1,})

    files_removed = set()
    for f in fnmatch.filter(pytest.fake_file_list, file_match):
        files_removed.add(str(pathlib.Path(f)))

    files = test_group.get_file_list()
    # Make sure the files actually exist first
    assert files.issuperset(files_removed)

    test_group.excludes.add(filt2)
    # Re-run with the exclusion filter.
    files = test_group.get_file_list()

    assert len(files_removed) > 0
    assert len(files) > 0
    assert files.isdisjoint(files_removed)
