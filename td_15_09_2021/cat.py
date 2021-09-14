from typing import List
from pathlib import Path
from argparse import ArgumentParser


def cat(files: List[Path]) -> None:
    for file in files:
        print(file.read_text())


if __name__ == "__main__":
    parser = ArgumentParser('A `cat` UNIX utility in Python')
    parser.add_argument('files', type=str, nargs='+', help='The files to read.')
    args = parser.parse_args()
    cat([Path(file) for file in args.files])
