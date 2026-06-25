# flash_card_service.py
# Created: 6/25/2026
# Last Edited: 6/25/2026
# Author: John Wesley Thompson

from createcards.flash_card import FlashCard, Sense, Word
from createcards.sentence_generator import OpenAISentenceGenerator

import json
from gtts import gTTS
import sqlite3

class FlashCardService:
    '''Services class to help construct FlashCard objects from different 
    sources.'''

    def __init__(
        self, 
        db_conn: sqlite3.Connection, 
        sentence_generator: OpenAISentenceGenerator
    ):
        self.db_conn = db_conn
        self.sentence_generator = sentence_generator

    def create_flash_cards(self, words: list[Word], print_progress: bool = True) -> list[FlashCard]:
        '''Creates of a list of FlashCard objects, querying the dictionary 
        database, generating sentences, and generating audio.'''

        # Database querying ---------------------------------------------------
        entry_ids: list[int | None] = []
        spellings: list[list[str]] = []
        readings: list[list[str]]= []
        senses: list[list[Sense]] = []

        if print_progress:
            print("-----------Gathering entries from database-----------")

        db_cursor = self.db_conn.cursor()
        for word in words:
            if not word.spelling and not word.reading: 
                raise ValueError("Empty lines in the input file are not allowed.")

            elif not word.spelling:
                db_cursor.execute(
                    """
                    SELECT readings.entry_id 
                    FROM readings
                    WHERE readings.reading = ?
                    """,
                    (word.reading,)
                )

            elif not word.reading:
                db_cursor.execute(
                    """
                    SELECT spellings.entry_id
                    FROM spellings
                    WHERE spellings.spelling = ?
                    """,
                    (word.spelling,)
                )

            # both reading and spelling is given
            else: 
                db_cursor.execute(
                    """
                    SELECT spellings.entry_id 
                    FROM spellings 
                    JOIN readings USING (entry_id)
                    WHERE spellings.spelling = ? AND readings.reading = ?
                    """,
                    (word.spelling, word.reading)
                )

            # No result was found
            row = db_cursor.fetchone()
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
            db_cursor.execute(
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

            row = db_cursor.fetchone()

            entry_ids.append(entry_id)
            spellings.append(json.loads(row['spellings']))
            readings.append(json.loads(row['readings']))
            senses.append([
                Sense(sense['sense_id'], sense['glosses']) 
                for sense in json.loads(row['senses'])
            ])

        # openai sentence generation ------------------------------------------
        if print_progress:
            print("----------Generating sentences with OpenAI-----------")

        sentences = self.sentence_generator.generate_sentences(words)

        # gTTs audio generation -----------------------------------------------
        word_audio_paths: list[str] = []
        sentence_audio_paths: list[str] = []

        if print_progress:
            print("-----Generating audio with Google Text-to-Speech-----")

        for i, word in enumerate(words):
            word_audio_path = f"{entry_ids[i] or 'unfound_entry'}_word.mp3"
            sentence_audio_path = f"{entry_ids[i] or 'unfound_entry'}_sentences.mp3"

            gtts_obj = gTTS(text=(word.reading or word.spelling), lang='ja', slow=False)
            gtts_obj.save(word_audio_path)

            gtts_obj = gTTS(text=sentences[i], lang='ja', slow=False)
            gtts_obj.save(sentence_audio_path)

            word_audio_paths.append(word_audio_path)
            sentence_audio_paths.append(sentence_audio_path)

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
