# jmdict_db.py
# Created: 6/18/2026
# Last Edited: 6/19/2026
# Author: John Wesley Thompson

import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path

DB_PATH = Path("data/jmdict.db")
XML_PATH = Path("data/JMdict_e")


db_connection = sqlite3.connect(DB_PATH)
cursor = db_connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS spellings (
        spelling_id INTEGER PRIMARY KEY,
        entry_id INTEGER NOT NULL,
        spelling TEXT NOT NULL
    );
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS readings (
        reading_id INTEGER PRIMARY KEY,
        entry_id INTEGER NOT NULL,
        reading TEXT NOT NULL
    );
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS senses (
        sense_id INTEGER PRIMARY KEY,
        entry_id INTEGER NOT NULL
    );
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS glosses (
        gloss_id INTEGER PRIMARY KEY,
        entry_id INTEGER NOT NULL,
        sense_id INTEGER NOT NULL,
        gloss TEXT NOT NULL,
        FOREIGN KEY(sense_id) REFERENCES senses(sense_id)
    );
    """
)

tree = ET.parse(XML_PATH)
root = tree.getroot()

db_connection.execute("BEGIN")

for entry in root.findall("entry"):
    entry_id = int(entry.findtext("ent_seq"))

    # insert entry
    # cursor.execute(
    #     "INSERT OR IGNORE INTO entries(entry_id) VALUES (?)",
    #     (ent_seq,)
    # )

    # insert spelling
    for keb in entry.findall("k_ele/keb"):
        cursor.execute (
            "INSERT INTO spellings (entry_id, spelling) VALUES (?, ?)",
            (entry_id, keb.text)
        )

    # insert readings
    for reb in entry.findall("r_ele/reb"):
        cursor.execute(
            "INSERT INTO readings (entry_id, reading) VALUES (?, ?)",
            (entry_id, reb.text)
        )

    # establish sense and glosses
    for sense in entry.findall("sense"):
        cursor.execute(
            "INSERT INTO senses (entry_id) VALUES (?)",
            (entry_id,)
        )

        sense_id = cursor.lastrowid

        for gloss in sense.findall("gloss"):
            cursor.execute(
                "INSERT INTO glosses (entry_id, sense_id, gloss) VALUES (?, ?, ?)",
                (entry_id, sense_id, gloss.text)
            )

db_connection.commit()
db_connection.close()

# <entry>
    # <ent_seq>1000090</ent_seq>
    # <k_ele>
        # <keb>○</keb>
    # </k_ele>
    # <k_ele>
        # <keb>〇</keb>
        # </k_ele>
        # <r_ele>
        # <reb>まる</reb>
        # </r_ele>
    # <sense>
        # <pos>noun (common) (futsuumeishi)</pos>
        # <xref>丸・まる・1</xref>
        # <s_inf>sometimes used for zero</s_inf>
        # <gloss xml:lang="eng">circle</gloss>
    # </sense>
    # <sense>
        # <pos>noun (common) (futsuumeishi)</pos>
        # <xref>二重丸</xref>
        # <s_inf>when marking a test, homework, etc.</s_inf>
        # <gloss xml:lang="eng">"correct"</gloss>
        # <gloss xml:lang="eng">"good"</gloss>
        # </sense>
    # <sense>
        # <pos>unclassified</pos>
        # <xref>〇〇・1</xref>
        # <s_inf>placeholder used to censor individual characters or indicate a space to be filled in</s_inf>
        # <gloss xml:lang="eng">*</gloss>
        # <gloss xml:lang="eng">_</gloss>
    # </sense>
    # <sense>
        # <pos>noun (common) (futsuumeishi)</pos>
        # <xref>句点</xref>
        # <gloss xml:lang="eng">period</gloss>
        # <gloss xml:lang="eng">full stop</gloss>
    # </sense>
    # <sense>
        # <pos>noun (common) (futsuumeishi)</pos>
        # <xref>半濁点</xref>
        # <gloss xml:lang="eng">handakuten (diacritic)</gloss>
    # </sense>
# </entry>

# <entry>
#     <ent_seq>1606840</ent_seq>
#     <k_ele>
#         <keb>割り勘</keb>
#         <ke_pri>news2</ke_pri>
#         <ke_pri>nf41</ke_pri>
#         <ke_pri>spec2</ke_pri>
#     </k_ele>
#     <k_ele>
#         <keb>割勘</keb>
#     </k_ele>
#     <r_ele>
#         <reb>わりかん</reb>
#         <re_pri>news2</re_pri>
#         <re_pri>nf41</re_pri>
#         <re_pri>spec2</re_pri>
#     </r_ele>
#     <r_ele>
#         <reb>ワリカン</reb>
#         <re_nokanji/>
#     </r_ele>
#     <sense>
#         <pos>&n;</pos>
#         <xref>割り前勘定</xref>
#         <misc>&abbr;</misc>
#         <gloss>splitting the cost</gloss>
#         <gloss>splitting the bill</gloss>
#         <gloss>Dutch treat</gloss>
#     </sense>
# </entry>

