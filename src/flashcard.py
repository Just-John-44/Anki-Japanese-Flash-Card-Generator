# flashcard.py
# Created: 8/9/2025
# Last Edited: 6/24/2026
# Author: John Wesley Thompson

from dataclasses import dataclass
from typing import Final, NamedTuple
from sentence_generator import OpenAISentenceGenerator
from sentence_generator import PROMPT_HEADER

from gtts import gTTS
import json


class Word(NamedTuple):
    spelling: str
    reading: str


class FlashCard:

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
    def TSVString(self) -> str:
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
            f"{";\n".join([', '.join(sense.glosses) for sense in self.senses])}\t"
            f"{self.sentences}\t"
            f"[sound:{self.reading_audio_path}]\t"
            f"[sound:{self.sentences_audio_path}]"
        )

        return tsv_string.replace('\n', "<br>")


class Sense:
    '''A class that represents a meaning of a word (a sense)'''

    def __init__(self, id: int, gloss_list: str):
        self.sense_id = id          # The id of the sense in the JMdict database
        self.glosses = gloss_list   # different ways a sense is expressed with language

    def __eq__(self, other):
        if not isinstance(other, Sense):
            return NotImplemented

        return (
            self.sense_id == other.sense_id and self.glosses == other.glosses
        )


    # a sense may contain more information in the future like part of 
    # speech or a context that the sense is used in

class FlashCardService:

    def __init__(self, db_conn, sentence_generator):
        self.db_conn = db_conn
        self.db_cursor = db_conn.cursor()
        self.sentence_generator = sentence_generator

    def createFlashCards(self, words: list[Word], print_progress: bool = True) -> list[FlashCard]:

        entry_ids: list[int] = []
        spellings: list[str] = []
        readings: list[str]= []
        senses: list[str] = []

        if print_progress:
            print("-----------Gathering entries from database-----------")

        for word in words:
            if not word.spelling and not word.reading: 
                continue

            elif not word.spelling:
                self.db_cursor.execute(
                    """
                    SELECT readings.entry_id 
                    FROM readings
                    WHERE readings.reading = ?
                    """,
                    (word.reading,)
                )

            elif not word.reading:
                self.db_cursor.execute(
                    """
                    SELECT spellings.entry_id
                    FROM spellings
                    WHERE spellings.spelling = ?
                    """,
                    (word.spelling,)
                )

            # both reading and spelling is given
            else: 
                self.db_cursor.execute(
                    """
                    SELECT spellings.entry_id 
                    FROM spellings 
                    JOIN readings USING (entry_id)
                    WHERE spellings.spelling = ? AND readings.reading = ?
                    """,
                    (word.spelling, word.reading)
                )

            # No result was found
            row = self.db_cursor.fetchone()
            if row is None:
                entry_ids.append(None)
                spellings.append([])
                readings.append([])
                senses.append([])
                print(f"-!!!-No entry found for {word.spelling or word.reading}-----")
                continue

            # In the case the user enters an ambiguous vocab word, the first 
            # match will be chosen. This should only happen when the user 
            # doesn't provide either a reading or a spelling
            entry_id = row['entry_id']

            # One big query with subqueries to gather information for one card
            self.db_cursor.execute(
                """
                SELECT 
                (
                    SELECT json_group_array(DISTINCT spelling)
                    FROM spellings
                    WHERE entry_id = ?1
                ) AS spellings,

                (
                    SELECT json_group_array(DISTINCT reading)
                    FROM readings
                    WHERE entry_id = ?1
                ) AS readings,

                (
                    SELECT json_group_array(
                        json_object(
                            'sense_id', sense_id,
                            'glosses', json(glosses)
                        )
                    )
                    FROM 
                    (
                        SELECT
                            sense_id,
                            json_group_array(DISTINCT gloss) AS glosses
                        FROM glosses
                        WHERE entry_id = ?1
                        GROUP BY sense_id
                        ORDER BY sense_id
                    )
                ) AS senses
                """,
                (entry_id,)
            )

            row = self.db_cursor.fetchone()

            entry_ids.append(entry_id)
            spellings.append(json.loads(row['spellings']))
            readings.append(json.loads(row['readings']))
            senses.append([Sense(sense['sense_id'], sense['glosses']) for sense in json.loads(row['senses'])])

        # openai sentence generation ------------
        if print_progress:
            print("----------Generating sentences with OpenAI-----------")

        sentences = self.sentence_generator.generateSentences(PROMPT_HEADER, words)

        # gTTs audio generation -----------------
        word_audio_paths: list[str] = []
        sentence_audio_paths: list[str] = []

        if print_progress:
            print("-----Generating audio with Google Text-to-Speech-----")

        for i, word in enumerate(words):
            word_audio_path = f"{entry_ids[i]}_word.mp3"
            sentence_audio_path = f"{entry_ids[i]}_sentences.mp3"

            gtts_obj = gTTS(text=(word.reading or word.spelling), lang='ja', slow=False)
            gtts_obj.save(word_audio_path)

            gtts_obj = gTTS(text=sentences[i], lang='ja', slow=False)
            gtts_obj.save(sentence_audio_path)

            word_audio_paths.append(word_audio_path)
            sentence_audio_paths.append(sentence_audio_path)

        print(len(entry_ids))
        print(len(spellings))
        print(len(readings))
        print(len(senses))
        print(len(sentences))
        print(len(word_audio_paths))
        print(len(sentence_audio_paths))

        flash_cards = [
            FlashCard(*values) for values in zip(
                spellings,
                readings,
                senses,
                sentences,
                word_audio_paths,
                sentence_audio_paths
            )
        ]

        return flash_cards
