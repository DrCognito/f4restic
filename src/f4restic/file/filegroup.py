import pathlib
import f4restic.file.discovery as discovery
from typing import Set, Tuple, List


class FileGroup:
    def __init__(
        self, *, filters: Set[Tuple[pathlib.Path, str, bool]] = None,
    ):
        """[summary]

        :param filters: [description], defaults to None
        :type filters: Set[Tuple(pathlib.Path, str, bool)], optional
        """
        if filters:
            self.filters = filters
        else:
            self.filters = set()

    def get_file_list(self) -> List[str]:
        out = []
        for path, pattern, recursive in self.filters:
            out.extend(discovery.filtered_files(path, pattern, recursive))

        return out
