import sqlite3
import os

def setup_database():
    db_path = 'aathichoodi.db'
    
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aathichoodi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tamil_text TEXT NOT NULL,
            transliteration TEXT NOT NULL,
            english_meaning TEXT NOT NULL
        )
    ''')

    # Clear existing data if any to avoid duplicates on multiple runs
    cursor.execute('DELETE FROM aathichoodi')

    # Aathichoodi data (Uyir Varkam - Vowels series by Avvaiyar)
    data = [
        ("அறம் செய விரும்பு", "Aram seya virumbu", "Desire to do righteous deeds."),
        ("ஆறுவது சினம்", "Aaruvathu sinam", "Anger is to be controlled."),
        ("இயல்வது கரவேல்", "Iyalvathu karavel", "Do not hide what you can give."),
        ("ஈவது விலக்கேல்", "Eevathu vilakkel", "Do not prevent charity."),
        ("உடையது விளம்பேல்", "Udaiyathu vilambel", "Do not boast about your possessions."),
        ("ஊக்கமது கைவிடேல்", "Ookkamathu kaividel", "Do not give up enthusiasm/hope."),
        ("எண் எழுத்து இகழேல்", "En ezhuththu igazhel", "Do not despise numbers and letters (education)."),
        ("ஏற்பது இகழ்ச்சி", "Erpathu igazhchi", "Begging is disgraceful."),
        ("ஐயம் இட்டு உண்", "Aiyam ittu un", "Share food with the needy before you eat."),
        ("ஒப்புரவு ஒழுகு", "Oppuravu ozhugu", "Act virtuously and in accordance with the world."),
        ("ஓதுவது ஒழியேல்", "Othuvathu ozhiyel", "Never stop learning."),
        ("ஔவியம் பேசேல்", "Auviyam pesel", "Do not speak enviously."),
        ("அஃகஞ் சுருக்கேல்", "Akhkan churukkel", "Do not cheat in measuring grains.")
    ]

    # Insert data
    cursor.executemany('''
        INSERT INTO aathichoodi (tamil_text, transliteration, english_meaning)
        VALUES (?, ?, ?)
    ''', data)

    # Commit and close
    conn.commit()
    print(f"Successfully created database '{db_path}' and added {len(data)} Aathichoodi quotes.")
    
    # Verify and print sample
    cursor.execute('SELECT * FROM aathichoodi LIMIT 3')
    rows = cursor.fetchall()
    print("\nSample data from database:")
    for row in rows:
        print(f"ID: {row[0]} | Tamil: {row[1]} | Transliteration: {row[2]} | Meaning: {row[3]}")

    conn.close()

if __name__ == '__main__':
    setup_database()
