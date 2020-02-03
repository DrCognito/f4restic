import pathlib
from typing import Set, Tuple


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
