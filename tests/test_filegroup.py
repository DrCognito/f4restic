import f4restic.file.filegroup as f4rgroup
import pathlib


def test_filegroup_filter_basic1():
    pair1 = (pathlib.Path("/fake/text.txt"), "*text", False)
    pair2 = (pathlib.Path("/fake/text.txt"), "*text", True)

    test_group = f4rgroup.FileGroup(filters={pair1,})

    assert pair1 in test_group.filters

    test_group.filters.add(pair2)

    assert pair2 in test_group.filters


def test_filegroup_filter_basic2():
    pair2 = (pathlib.Path("/fake/text.txt"), "*text", True)

    test_group = f4rgroup.FileGroup()
    test_group.filters.add(pair2)
    assert pair2 in test_group.filters
