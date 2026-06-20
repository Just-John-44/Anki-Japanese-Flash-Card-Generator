# John Wesley Thompson
# Created: 8/9/2025
# Last Edited: 6/20/2026
# flashcard.py

from dataclasses import dataclass
from typing import Final
from dictionary_entry import DictionaryEntry

IDEOGRAPHIC_SPACE: Final[str] = "\u3000"

@dataclass
class FlashCard:
    dict_entry = DictionaryEntry()
    sentences: str = ""
    reading_audio_path: str = ""
    sentence_audio_path: str = ""

    @property
    def TSVString(self) -> str:
        if self.dict_entry.spellings:
            tsv_string = (
                f"{'・'.join(self.dict_entry.spellings)} | "
                f"{'・'.join(self.dict_entry.readings)}\t"
            )
        else:
            tsv_string = (
                f"{'・'.join(self.dict_entry.readings)}\t"
            )

        tsv_string += (
            f"{";\n".join([sense.glosses for sense in self.dict_entry.senses])}\t"
            f"{self.sentences}\t"
            f"[sound:{self.word_audio_path}]\t"
            f"[sound:{self.sentence_audio_path}]"
        )

        return tsv_string.replace('\n', "<br>")

    def isMissingFields(self) -> bool:
        # card can have no kanji if it has kana
        if (self.spelling == "" and self.reading == "" or 
            self.reading == "" or
            self.definition == "" or
            self.sentences == "" or
            self.word_audio_path == "" or
            self.sentence_audio_path == ""):
            return True

        return False