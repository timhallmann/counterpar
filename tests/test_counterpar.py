"""Tests for counterpar.__init__"""

import pytest

from counterpar import counterpar

TEXT = """(first paragraph
hello world

'second ] paragraph

third paragraph []][

fourth paragraph)
"""

TEXT1 = TEXT.split("\n")
TEXT2 = ["---\n" if not l else l + "\n" for l in TEXT1]

counterpar_data = [
    ([], "", None, None, None, []),
    (TEXT1, "'", None, None, None, [
        (4, 4, "'second ] paragraph")]),
    (TEXT1, "(", None, None, None, [
        (1, 2, "(first paragraphhello world"),
        (8, 8, "fourth paragraph)")]),
    (TEXT1, "(", "(", None, None, [
        (1, 2, "(first paragraphhello world")]),
    (TEXT1, "(", None, None, None, [
        (1, 2, "(first paragraphhello world"),
        (8, 8, "fourth paragraph)")]),
    (TEXT1, "[", None, None, True, [
        (4, 4, "'second ] paragraph")]),
    (TEXT1, "[", None, None, None, [
        (4, 4, "'second ] paragraph"),
        (6, 6, "third paragraph []][")]),
    (TEXT2, "'", None, "---", None, [
        (4, 4, "'second ] paragraph\n")])
    ]

@pytest.mark.parametrize(
    "lines,opening_symbol,closing_symbol,paragraph_separator,ignore_order,expected",
    counterpar_data)
def test_counterpar_results( # pylint: disable=too-many-arguments
        lines,
        opening_symbol,
        closing_symbol,
        paragraph_separator,
        ignore_order,
        expected):
    """Test counterpar.counterpar"""
    assert list(counterpar(
        lines, opening_symbol, closing_symbol=closing_symbol,
        paragraph_separator=paragraph_separator, ignore_order=ignore_order
        )) == expected
