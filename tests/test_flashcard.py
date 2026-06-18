# test_flashcard.py
# Created: 6/18/2026
# Last Edited: 6/18/2026
# Author: John Wesley Thompson

import pytest

from src.flashcard import FlashCard
from src.flashcard import IDEOGRAPHIC_SPACE


@pytest.mark.parametrize("writing, kana", [
    ("家", "いえ"),
    ("車", "くるま"),
    ("犬", "いぬ")
])
def test_constructor(writing, kana):
    card = FlashCard((writing, kana))
    assert card.writing == writing
    assert card.kana == kana

def test_setDefinition():
    pass

def test_setSentences():
    pass

def test_setWordAudioFilepath():
    pass

def test_setSentenceAudioFilepath():
    pass

def test_repr():
    pass

def test_TSVString():
    pass

def test_isMissingFields():
    pass

