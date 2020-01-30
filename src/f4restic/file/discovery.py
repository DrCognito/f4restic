import pathlib
from typing import List


def filtered_files(
    base_dir: pathlib.Path, pattern: str, recursive: bool
) -> List[pathlib.Path]:

    glob = pathlib.Path.rglob if recursive else pathlib.Path.glob

    return [str(x) for x in glob(base_dir, pattern)]
