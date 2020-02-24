import pathlib
import f4restic.file.discovery as discovery
from typing import Set, Tuple, List


class FileGroup:
    def __init__(
        self,
        *,
        includes: Set[Tuple[pathlib.Path, str, bool]] = None,
        excludes: Set[Tuple[pathlib.Path, str, bool]] = None,
    ):
        """[summary]

        :param includes: List of glob filters to be applied sequentially, defaults to None
        :type includes: Set[Tuple(pathlib.Path, str, bool)], optional
        """
        if includes:
            self.includes = includes
        else:
            self.includes = set()

        if excludes:
            self.excludes = excludes
        else:
            self.excludes = set()

    def get_file_list(self) -> Set[str]:
        out = []
        for path, pattern, recursive in self.includes:
            out.extend(discovery.filtered_files(path, pattern, recursive))

        out = set(out)

        # Build an exclude list with the same methods.
        # This is potentially slow as of course we hit the fs twice and then subtract.
        # This minimally allows for code reuse with filtered_files
        excl = []
        for path, pattern, recursive in self.excludes:
            excl.extend(discovery.filtered_files(path, pattern, recursive))
        excl = set(excl)

        out.difference_update(excl)
        return out
