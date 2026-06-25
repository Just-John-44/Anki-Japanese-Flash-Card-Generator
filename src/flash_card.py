# flashcard.py
# Created: 8/9/2025
# Last Edited: 6/25/2026
# Author: John Wesley Thompson

from typing import NamedTuple


class Word(NamedTuple):
    spelling: str
    reading: str


class Sense:
    '''Class that represents a meaning of a word (a sense)'''

    def __init__(self, sense_id: int, glosses: list[str]):
        self.sense_id = sense_id    # The id of the sense in the JMdict database
        self.glosses = glosses      # different ways a sense is expressed with language

    def __eq__(self, other):
        if not isinstance(other, Sense):
            return NotImplemented

        return (
            self.sense_id == other.sense_id and self.glosses == other.glosses
        )

    # a sense may contain more information in the future like part of 
    # speech or a context that the sense is used in


class FlashCard:
    '''Object representing all of the data needed for an Anki flash card'''

    def __init__(
        self,
        readings: list[str], 
        spellings: list[str], 
        senses: list[Sense], 
        sentences: str, 
        reading_audio_path: str, 
        sentences_audio_path: str
    ):
        self.readings = readings
        self.spellings = spellings
        self.senses = senses
        self.sentences = sentences
        self.reading_audio_path = reading_audio_path
        self.sentences_audio_path = sentences_audio_path

    @property
    def tsv_string(self) -> str:
        '''TSV representation of the FlashCard object'''

        if self.spellings:
            tsv_string = (
                f"{'・'.join(self.spellings)} | "
                f"{'・'.join(self.readings)}\t"
            )
        else:
            tsv_string = (
                f"{'・'.join(self.readings)}\t"
            )

        tsv_string += (
            f"{';\n'.join([', '.join(sense.glosses) for sense in self.senses])}\t"
            f"{self.sentences}\t"
            f"[sound:{self.reading_audio_path}]\t"
            f"[sound:{self.sentences_audio_path}]"
        )

        return tsv_string.replace('\n', "<br>")
