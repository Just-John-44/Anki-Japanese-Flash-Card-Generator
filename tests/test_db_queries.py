# test_db_queries.py
# Created: 6/20/2026
# Last Edited: 6/20/2026
# Author: John Wesley Thompson

import pytest
import sqlite3

from src.dictionary_entry import DictionaryEntry, Sense, findEntry

@pytest.mark.parametrize(
    "spelling, reading, entry_id, spellings, readings, senses", [
# ===== queries with both spelling and reading (most common) ==================
        (
            "犬", "いぬ",
            1258330,
            ['犬', '狗'],
            ['いぬ', 'イヌ'],
            [
                Sense(30311, 'dog (Canis (lupus) familiaris), canine'),
                Sense(30312, 'squealer, rat, snitch, informer, informant, spy'),
                Sense(30313, 'loser, asshole'),
                Sense(30314, 'counterfeit, inferior, useless, wasteful')
            ]
        ),
        # query with 1st spelling and 1st reading
        (
            "割り勘", "わりかん", 
            1606840,
            ['割り勘', '割勘'],
            ['わりかん', 'ワリカン'],
            [
                Sense(75761, 'splitting the cost, splitting the bill, Dutch treat')
            ]
        ),
        # query with 2nd spelling and 2nd reading
        (
            "割勘", "ワリカン", 
            1606840,
            ['割り勘', '割勘'],
            ['わりかん', 'ワリカン'],
            [
                Sense(75761, 'splitting the cost, splitting the bill, Dutch treat')
            ]
        ),
        # query with 1st spelling and 2nd reading
        (
            "割り勘", "ワリカン", 
            1606840,
            ['割り勘', '割勘'],
            ['わりかん', 'ワリカン'],
            [
                Sense(75761, 'splitting the cost, splitting the bill, Dutch treat')
            ]
        ),
        # query with 2nd spelling and 1st reading
        (
            "割り勘", "わりかん", 
            1606840,
            ['割り勘', '割勘'],
            ['わりかん', 'ワリカン'],
            [
                Sense(75761, 'splitting the cost, splitting the bill, Dutch treat')
            ]
        ), 
# ===== queries with no spelling or no reading ================================
        (
            "", "コンクリート", 
            1051860,
            ['混凝土'],
            ['コンクリート'],
            [
                Sense(6051, 'concrete')
            ]
        ),
        # query with first reading only
        (
            "", "わりかん", 
            1606840,
            ['割り勘', '割勘'],
            ['わりかん', 'ワリカン'],
            [
                Sense(75761, 'splitting the cost, splitting the bill, Dutch treat')
            ]
        ),
        # query with second spelling only
        (
            "", "ワリカン", 
            1606840,
            ['割り勘', '割勘'],
            ['わりかん', 'ワリカン'],
            [
                Sense(75761, 'splitting the cost, splitting the bill, Dutch treat')
            ]
        ),
        (
            "犬", "",
            1258330,
            ['犬', '狗'],
            ['いぬ', 'イヌ'],
            [
                Sense(30311, 'dog (Canis (lupus) familiaris), canine'),
                Sense(30312, 'squealer, rat, snitch, informer, informant, spy'),
                Sense(30313, 'loser, asshole'),
                Sense(30314, 'counterfeit, inferior, useless, wasteful')
            ]
        ),
# ===== incorrect queries (queries with valid input, but should fail) ========
        # mismatched vocabulary
        (
            "図書館", "くるま", 
            None,
            [],
            [],
            []
        ),
        # unconventional spelling
        (
            "図書かん", "としょかん", 
            None,
            [],
            [],
            []
        ),
# ===== garbage queries ======================================================
        # 2 readings given, each for a different word; reading in spelling field
        (
            "いぬ", "ねこ", 
            None,
            [],
            [],
            []
        ),
        # 2 of the same readings given; reading in spelling field
        (
            "くるま", "くるま", 
            None,
            [],
            [],
            []
        ),
        # 1 reading given in the spelling field
        (
            "くるま", "", 
            None,
            [],
            [],
            []
        ),
        # erroneus input
        (
            "qwerty", "abdc", 
            None,
            [],
            [],
            []
        ),
        # empty
        (
            "", "", 
            None,
            [],
            [],
            []
        )
    ]
)
def test_query_input_variations(spelling, reading, entry_id, spellings, readings, senses):
    db_conn = sqlite3.connect("data/jmdict.db")
    cursor = db_conn.cursor()

    word = (spelling, reading)
    myentry = findEntry(word, cursor)

    assert myentry.entry_id == entry_id
    # if spellings != "":
    assert myentry.spellings == spellings
    # if readings != "":
    assert myentry.readings == readings
    assert myentry.senses == senses