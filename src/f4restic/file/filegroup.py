import pathlib
import f4restic.file.discovery as discovery
from typing import Set, Tuple, List


class FileGroup:
    def __init__(
        self, *, includes: Set[Tuple[pathlib.Path, str, bool]] = None,
    ):
        """[summary]

        :param includes: List of glob filters to be applied sequentially, defaults to None
        :type includes: Set[Tuple(pathlib.Path, str, bool)], optional
        """
        if includes:
            self.includes = includes
        else:
            self.includes = set()

    def get_file_list(self) -> List[str]:
        out = []
        for path, pattern, recursive in self.includes:
            out.extend(discovery.filtered_files(path, pattern, recursive))

        return out
