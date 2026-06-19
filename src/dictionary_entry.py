# dictionary_entry.py
# Created: 6/18/2026
# Last Edited: 6/19/2026
# Author: John Wesley Thompson

from dataclasses import dataclass, field

class Sense:
    '''A class that represents a meaning of a word (a sense)'''

    def __init__(self, id: int, gloss_list: str):
        self.sense_id = id          # The id of the sense in the JMdict database
        self.glosses = gloss_list   # different ways a sense is expressed with language

    # a sense may contain more information in the future like part of 
    # speech or a context that the sense is used in

@dataclass
class DictionaryEntry:
    '''A class that represents an entry in the JMdict_e database'''

    entry_id: int | None = None                         # The id of the entry in the JMdict database
    spellings: list[str] = field(default_factory=list)  # All ways the word can be written  ex.) 割り勘 vs. 割勘
    readings: list[str] = field(default_factory=list)   # The kana writings for the word    ex.) わりかん and ワリカン
    senses: list[str] = field(default_factory=list)     # The different meanings of a word  ex.) "bank" is a place to keep money, but also a landform along a river
