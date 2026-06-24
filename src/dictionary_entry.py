# dictionary_entry.py
# Created: 6/18/2026
# Last Edited: 6/20/2026
# Author: John Wesley Thompson

from dataclasses import dataclass, field

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


@dataclass
class DictionaryEntry:
    '''A class that represents an entry in the JMdict_e database'''

    entry_id: int | None = None                         # The id of the entry in the JMdict database
    spellings: list[str] = field(default_factory=list)  # All ways the word can be written  ex.) 割り勘 vs. 割勘
    readings: list[str] = field(default_factory=list)   # The kana writings for the word    ex.) わりかん and ワリカン
    senses: list[str] = field(default_factory=list)     # The different meanings of a word  ex.) "bank" is a place to keep money, but also a landform along a river


def findEntry(word, cursor):
    my_entry = DictionaryEntry()

    # if neither reading nor spelling is given
    if not word[0] and not word[1]: 
        return my_entry

    # if only the reading is given
    elif not word[0]:
        cursor.execute(
            """
            SELECT readings.entry_id 
            FROM readings
            WHERE readings.reading = ?
            """,
            (word[1],)
        )

    # if only the spelling is given
    elif not word [1]:
        cursor.execute(
            """
            SELECT spellings.entry_id
            FROM spellings
            WHERE spellings.spelling = ?
            """,
            (word[0],)
        )

    # both reading and spelling is given
    else: 
        cursor.execute(
            """
            SELECT spellings.entry_id 
            FROM spellings 
            JOIN readings 
            ON spellings.entry_id = readings.entry_id 
            WHERE spellings.spelling = ? AND readings.reading = ?
            """,
            (word[0], word[1])
        )
    row = cursor.fetchone()
    if row is None:
        return my_entry
    my_entry.entry_id = row[0] # grab the first matching entry "query should only return more than one match if the user entered a reading with multiple spellings or vice verse (an ambiguous vocab item)"

    # assign spellings
    cursor.execute(
        "SELECT spelling FROM spellings WHERE entry_id = ?",
        (my_entry.entry_id,)
    )
    my_entry.spellings = [x[0] for x in cursor.fetchall()]

    # assign readings
    cursor.execute(
        "SELECT reading FROM readings WHERE entry_id = ?",
        (my_entry.entry_id,)
    )
    my_entry.readings = [x[0] for x in cursor.fetchall()]

    # find sense ids
    cursor.execute(
        """
        SELECT sense_id 
        FROM senses 
        WHERE senses.entry_id = ?
        """,
        (my_entry.entry_id,)
    )
    sense_ids = [x[0] for x in cursor.fetchall()]

    # assign sense ids and find and assign glosses to sense objects
    for id in sense_ids:
        cursor.execute(
            """
            SELECT gloss 
            FROM glosses 
            WHERE glosses.sense_id = ?
            """,
            (id,)
        )
        my_entry.senses.append(Sense(id, ', '.join([x[0] for x in cursor.fetchall()])))

    return my_entry

# <entry>
#     <ent_seq>1578850</ent_seq>
#     <k_ele>
#         <keb>行く</keb>
#         <ke_pri>ichi1</ke_pri>
#     </k_ele>
#     <k_ele>
#         <keb>往く</keb>
#         <ke_inf>&rK;</ke_inf>
#     </k_ele>
#     <r_ele>
#         <reb>いく</reb>
#         <re_pri>ichi1</re_pri>
#     </r_ele>
#     <r_ele>
#         <reb>ゆく</reb>
#         <re_pri>ichi1</re_pri>
#     </r_ele>
#     <r_ele>
#         <reb>イク</reb>
#         <re_inf>&sk;</re_inf>
#     </r_ele>
#     <sense>
#         <pos>&v5k-s;</pos>
#         <pos>&vi;</pos>
#         <xref>来る・1</xref>
#         <gloss>to go</gloss>
#         <gloss>to move (towards)</gloss>
#         <gloss>to head (towards)</gloss>
#         <gloss>to leave (for)</gloss>
#     </sense>
#     <sense>
#         <pos>&v5k-s;</pos>
#         <pos>&vi;</pos>
#         <gloss>to move through</gloss>
#         <gloss>to travel across</gloss>
#         <gloss>to walk along (e.g. a road)</gloss>
#     </sense>
#     <sense>
#         <pos>&v5k-s;</pos>
#         <pos>&vi;</pos>
#         <gloss>to go (well, badly, etc.)</gloss>
#         <gloss>to proceed</gloss>
#         <gloss>to turn out</gloss>
#         <gloss>to get along</gloss>
#     </sense>
#     <sense>
#         <pos>&v5k-s;</pos>
#         <pos>&vi;</pos>
#         <s_inf>oft. as で〜</s_inf>
#         <gloss>to do (in a particular way)</gloss>
#         <gloss>to go (with; a choice)</gloss>
#         <gloss>to try</gloss>
#     </sense>
#     <sense>
#         <pos>&v5k-s;</pos>
#         <pos>&vi;</pos>
#         <gloss>to pass (of time, seasons, etc.)</gloss>
#         <gloss>to go by</gloss>
#     </sense>
#     <sense>
#         <pos>&v5k-s;</pos>
#         <pos>&vi;</pos>
#         <gloss>to stream</gloss>
#         <gloss>to flow</gloss>
#     </sense>
#     <sense>
#         <pos>&v5k-s;</pos>
#         <pos>&vi;</pos>
#         <s_inf>usu. written as 逝く</s_inf>
#         <gloss>to die</gloss>
#         <gloss>to pass away</gloss>
#     </sense>
#     <sense>
#         <pos>&v5k-s;</pos>
#         <pos>&vi;</pos>
#         <gloss>to reach (a stage, extent, age, etc.)</gloss>
#         <gloss>to get to</gloss>
#         <gloss>to go (so far as ...)</gloss>
#     </sense>
#     <sense>
#         <pos>&v5k-s;</pos>
#         <pos>&vi;</pos>
#         <gloss>to reach (of information, instructions, wind, etc.)</gloss>
#         <gloss>to arrive</gloss>
#     </sense>
#     <sense>
#         <pos>&aux-v;</pos>
#         <pos>&v5k-s;</pos>
#         <misc>&uk;</misc>
#         <s_inf>after the -te form of a verb; い sometimes omitted in casual speech</s_inf>
#         <gloss>to continue ...</gloss>
#         <gloss>to go on ...</gloss>
#         <gloss>to (progress) steadily</gloss>
#         <gloss>to gradually ...</gloss>
#         <gloss>to progressively ...</gloss>
#     </sense>
#     <sense>
#         <pos>&v5k-s;</pos>
#         <pos>&vi;</pos>
#         <misc>&uk;</misc>
#         <misc>&col;</misc>
#         <s_inf>oft. written as イク</s_inf>
#         <gloss>to have an orgasm</gloss>
#         <gloss>to come</gloss>
#         <gloss>to cum</gloss>
#     </sense>
#     <sense>
#         <pos>&v5k-s;</pos>
#         <pos>&vi;</pos>
#         <misc>&uk;</misc>
#         <misc>&sl;</misc>
#         <gloss>to trip</gloss>
#         <gloss>to get high</gloss>
#         <gloss>to have a drug-induced hallucination</gloss>
#     </sense>
# </entry