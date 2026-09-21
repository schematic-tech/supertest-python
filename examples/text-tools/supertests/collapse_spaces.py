from schematic import *

from text_tools.text import collapse_spaces


@supertest
def collapsing_spaces_again_changes_nothing(text: str):
    once = collapse_spaces(text)
    twice = collapse_spaces(once)

    assert twice == once
