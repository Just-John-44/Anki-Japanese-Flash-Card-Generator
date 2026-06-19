
import sqlite3

db_connection = sqlite3.connect("data/jmdict.db")
cursor = db_connection.cursor()

word = "割り勘"

cursor.execute("""
    SELECT entry_id
    FROM spellings
    WHERE spelling = ?
""", (word,)
)

result = cursor.fetchone()
if not result: 
    print("not found.")
    exit()

ent_seq = result[0]

# 2. get readings
cursor.execute("""
    SELECT reading
    FROM readings
    WHERE entry_id = ?
""", (ent_seq,))
readings = [r[0] for r in cursor.fetchall()]

# 3. get senses + glosses
cursor.execute("""
    SELECT s.id, g.gloss
    FROM senses s
    JOIN glosses g ON g.sense_id = s.id
    WHERE s.entry_id = ?
""", (ent_seq,))

sense_data = cursor.fetchall()

db_connection.close()

# 4. print structured result
print("WORD:", word)
print("READINGS:", readings)
print("SENSES:")

for sense_id, gloss in sense_data:
    print(f"  Sense {sense_id}: {gloss}")

db_connection.close()