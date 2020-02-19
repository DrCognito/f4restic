import pathlib
from typing import List


def filtered_files(
    base_dir: pathlib.Path, pattern: str, recursive: bool
) -> List[pathlib.Path]:

    glob = pathlib.Path.rglob if recursive else pathlib.Path.glob

    out = []
    p: pathlib.Path
    for p in glob(base_dir, pattern):
        if p.is_dir() and recursive:
            # Add all the files in the directory
            # As we use glob it will perform recursive addition as well!
            out.extend([str(x) for x in glob(p, "*")])
        else:
            out.append(str(p))

    return out
