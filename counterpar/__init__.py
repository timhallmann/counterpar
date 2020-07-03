"""Find paragraphs that are missing the counterpart of a symbol."""

import re
from typing import Dict, Iterator, List, Optional, Tuple

from collections import namedtuple

__version__ = "0.1.0"
__all__ = ["counterpar", "COUNTERPARTS"]

COUNTERPARTS: Dict[str, str] = {
    "(": ")",
    ")": "(",
    "[": "]",
    "]": "[",
    "{": "}",
    "}": "{",
    "<": ">",
    ">": "<",
    '"`': '"\'',
    '"\'': '"`'
}
"""---will be replaced by the following statement---"""
try:
    __pdoc__ = {}
    __pdoc__["COUNTERPARTS"] = "\n".join([
        "```",
        "\n".join([f"{key} {value}" for key, value in COUNTERPARTS.items()]),
        "```"])
except Exception: # pylint: disable=broad-except
    pass


def counterpar(
        lines: Iterator[str],
        opening_symbol: str,
        closing_symbol: str = None,
        paragraph_separator: str = None,
        ignore_order: bool = False) -> Iterator[Tuple[int, int, str]]:
    """
    Find paragraphs that are missing the counterpart of a symbol.

    A paragraph is defined as the concatenation of lines between (exclusive)
    the two closest lines matching the `paragraph_separator` regex (or the
    start/end of the file).

    Line breaks are neither added nor removed; the paragraph is created by
    simply joining the respective lines together. This means that each line must
    have its own line break so that the paragraph created is the same as the
    original one (as is the case for `open` or `stdin`).

    Args:
        lines (Iterator[str]): Lines to search.
        opening_symbol (str): Opening symbol.
        closing_symbol (str, optional): Closing symbol. Defaults to None,
            meaning that the counterpart of the `opening_symbol` is guessed;
            if no match is found, the closing symbol is the opening symbol.
        paragraph_separator (str, optional): A line matching this regex ends the
            current paragraph. The following line begins the next paragraph.
            Defaults to None (empty line or only null or whitespace(s)).
        ignore_order (bool, optional): Ignore the order of opening_symbol and
            closing_symbol; compare only their counts. Defaults to False.

    Yields:
        Iterator[Tuple[int, int, str]]: The line number of the first and last
            line of the found paragraph and the paragraph itself.
    """

    if closing_symbol is None:
        closing_symbol = COUNTERPARTS.get(opening_symbol)
    par_separator = re.compile(paragraph_separator or "^[\0 ]*$")

    # Add an empty last line so that the last paragraph does not need to be
    # treated specially.
    def lines_generator() -> Iterator[Optional[str]]:
        for line in lines:
            yield line
        yield None

    par_start = 1
    par_lines: List[str] = []

    for line_number, line in enumerate(lines_generator()):
        if not (line is None or par_separator.match(line)):
            par_lines.append(line)
            continue

        par = "".join(par_lines)
        if not par: # Skip empty paragraphs.
            continue

        if closing_symbol is None:
            matching = not par.count(opening_symbol) % 2
        elif ignore_order:
            matching = par.count(opening_symbol) == par.count(closing_symbol)
        else:
            matching = check_symbol_order(par, opening_symbol, closing_symbol)

        if not matching:
            yield (par_start, line_number, par)

        par_start = line_number + 2
        par_lines = []

def check_symbol_order(par: str, opening_symbol: str, closing_symbol: str) -> bool:
    """Check order of symbols.

    a) Every opening_symbol has exactly one closing_symbol.
    b) Every closing_symbol has exactly one opening_symbol.
    c) That opening_symbol is before the closing_symbol.

    Args:
        par (str): Paragraph to check.
        opening_symbol (str): Opening symbol.
        closing_symbol (str): Closing symbol.

    Returns:
        bool: Whether all conditions are true.
    """

    count = 0
    for character in par:
        if character == opening_symbol:
            count += 1
        elif character == closing_symbol:
            count -= 1
            if count < 0:
                break
    return not count
