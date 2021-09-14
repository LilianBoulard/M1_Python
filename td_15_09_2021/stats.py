from typing import List, Dict, Tuple, Generator
from argparse import ArgumentParser
from pathlib import Path


def _get_words(text: str) -> Generator[str, None, None]:
    """
    Takes some text, and divides it to get the individual words.
    Handles the punctuation by default.
    """
    excluded_words: List[str] = ['\n', '']
    for word in text.split(' '):
        if word not in excluded_words:
            if not word.isalpha():
                # If there are special characters in the string,
                # filter them out.
                word = ''.join([
                    letter
                    for letter in word
                    if letter.isalpha()
                ])
            yield word


def _line_count(text: List[str]) -> int:
    """
    Returns the line count in a text.
    Does not count empty lines.
    """
    return len([
        line
        for line in text
        if line.strip() != ''  # Do not count empty lines
    ])


def _char_count(text: List[str]) -> int:
    """
    Returns a count of all the characters in a string,
    including special character, number, spaces, etc.
    but not line breaks.
    """
    return sum([len(line) for line in text])


def _word_count(text: str) -> int:
    return len(list(_get_words(text)))


def _most_frequent_words(text: str) -> Tuple[List[str], int]:
    word_count_mapping: Dict[str: int] = {}
    words = list(_get_words(text))
    for word in words:
        word = word.lower()
        if word in word_count_mapping.keys():
            word_count_mapping[word] += 1
        else:
            word_count_mapping[word] = 1
    # Sort the mapping by highest value
    word_count_mapping = dict(
        sorted(
            word_count_mapping.items(),
            key=lambda pair: pair[1],
            reverse=True,
        )
    )
    # Get the occurrences, and get the longest words with it
    _, occurrences = list(word_count_mapping.items())[0]
    most_frequent_words: List[str] = []
    for word, occ in word_count_mapping.items():
        if occ == occurrences:
            most_frequent_words.append(word)
        else:
            # AS they are sorted, as soon as we get a number with a different
            # occurrence count, we can get out of the loop.
            break
    return most_frequent_words, occurrences


def _longest_word(text: str) -> str:
    words = list(_get_words(text))
    # We store a tuple in memory: the longest word, and its length.
    longest_word, longest_word_length = words[0], len(words[0])
    for word in words:
        if len(word) > longest_word_length:
            longest_word, longest_word_length = word, len(word)
    return longest_word


def _most_frequent_letter(text: str) -> Tuple[str, int]:
    char_count_mapping: Dict[str, int] = {}
    for word in _get_words(text):
        word = word.lower()
        for char in word:
            if char in char_count_mapping.keys():
                char_count_mapping[char] += 1
            else:
                char_count_mapping[char] = 1
    # Sort the mapping by highest value
    char_count_mapping = dict(
        sorted(
            char_count_mapping.items(),
            key=lambda pair: pair[1],
            reverse=True,
        )
    )
    most_frequent_char, occurrences = list(char_count_mapping.items())[0]
    return most_frequent_char, occurrences


def _mean_word_count_per_line(text: List[str]) -> float:
    count_per_line: List[int] = []
    for line in text:
        count_per_line.append(len(list(_get_words(line))))
    return sum(count_per_line) / _line_count(text)


def _format_most_frequent_words(words: List[str]) -> str:
    words_quoted = [f"{word!r}" for word in words]
    first_words = words_quoted[:-1]
    last_word = words_quoted[-1]
    joint = ' and ' if len(words_quoted) > 1 else ''
    return f'{", ".join(first_words)}{joint}{last_word}'


def stats(file: Path) -> None:
    with file.open(mode='r', encoding='utf8') as fl:
        list_content: List[str] = [line.strip('\n') for line in fl.readlines()]
        # We'll reconstruct the full text instead of reading the file again.
        # We'll join the lines with spaces instead of line breaks to make
        # further analysis simpler
        text_content: str = ' '.join(list_content)

        most_frequent_words, most_frequent_word_occurrences = _most_frequent_words(text_content)
        most_frequent_letter, most_frequent_letter_occurrences = _most_frequent_letter(text_content)
        longest_word = _longest_word(text_content)

        print(
            f'Stats for file {str(file)!r}: \n'
            f'Line count: {_line_count(list_content)} (not counting empty lines) \n'
            f'Character count: {_char_count(list_content)} \n'
            f'Word count: {_word_count(text_content)} \n'
            f'Most frequent {"words" if len(most_frequent_words) > 1 else "word"}: '
            f'{_format_most_frequent_words(most_frequent_words)} '
            f'(with {most_frequent_word_occurrences} occurrences'
            f'{" each" if len(most_frequent_words) > 1 else ""}) \n'
            f'Longest word: {longest_word!r} (with {len(longest_word)} characters) \n'
            f'Mean word count per line: {_mean_word_count_per_line(list_content):.2f} \n'
            f'Most frequent letter: {most_frequent_letter!r} '
            f'(with {most_frequent_letter_occurrences} occurrences) \n'
        )


if __name__ == "__main__":
    parser = ArgumentParser('Statistics on a file')
    parser.add_argument('file', help='File to analyze', type=str, nargs=1)
    args = parser.parse_args()
    path = Path(args.file[0])
    if not path.exists():
        input("The specified file doesn't exist.")
    else:
        stats(path)
