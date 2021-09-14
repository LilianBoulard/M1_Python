from argparse import ArgumentParser
from typing import List
from pathlib import Path


def _merge_slices(slices: List[slice]) -> List[slice]:
    """
    Takes slices with overlapping parts,
    and combines them into continuous and unique slices.
    Also, sorts them.
    """
    indices: List[int] = []
    for slc in slices:
        indices.extend(list(range(slc.start, slc.stop)))

    clean_slices: List[slice] = []
    max_idx = max(indices)
    start = None  # Slice start
    stop = None  # Slice stop
    # These two are set to None when no slice is in the making

    # Not very optimized, but functional
    for i in range(max_idx + 2):
        if i in indices:
            if start is None:
                start = i
        else:
            if start is not None:
                stop = i
                clean_slices.append(slice(start, stop))
                start = None
                stop = None

    return clean_slices


def cut(sep_char: str, ranges: List[str], file_path: Path):
    # Convert the ranges to slices
    slices: List[slice] = []
    for rng in ranges:
        a, b = rng.split('-')
        slices.append(slice(int(a) - 1, int(b)))
    slices = _merge_slices(slices)

    with file_path.open(mode='r') as fl:
        for line in fl.readlines():
            # Remove line breaks
            line = line.strip('\n')
            result_parts: List[str] = []
            line_parts = line.split(sep_char)
            for slc in slices:
                result_parts.append(sep_char.join(line_parts[slc]))
            result = sep_char.join(result_parts)
            print(result)


if __name__ == "__main__":
    parser = ArgumentParser('A `cut` UNIX utility in Python')
    parser.add_argument('-d', nargs=1, type=str)
    parser.add_argument('-f', nargs=1, type=str)
    parser.add_argument('file', nargs=1, type=str)
    args = parser.parse_args()
    cut(args.d[0], args.f[0].split(','), Path(args.file[0]))
