import sqlite3
import urllib.request
import json
import os

def main():
    print("Downloading thirukkural.json...")
    req = urllib.request.Request('https://raw.githubusercontent.com/tk120404/thirukkural/master/thirukkural.json', headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    kurals_data = json.loads(res.read())['kural']

    print("Downloading detail.json...")
    req = urllib.request.Request('https://raw.githubusercontent.com/tk120404/thirukkural/master/detail.json', headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    detail_data = json.loads(res.read())

    # Build a mapping from kural_id to iyal and athigaaram
    kural_meta = {}
    for paal in detail_data[0]['section']['detail']:
        for iyal in paal['chapterGroup']['detail']:
            iyal_name = iyal['name']
            for athigaaram in iyal['chapters']['detail']:
                athigaaram_name = athigaaram['name']
                start = athigaaram['start']
                end = athigaaram['end']
                for k_id in range(start, end + 1):
                    kural_meta[k_id] = {
                        'iyal': iyal_name,
                        'athigaaram': athigaaram_name
                    }

    # Connect to krl.db to get Parimelazhagar's explanation (a_id = 29)
    print("Reading Parimelazhagar's explanations from krl.db...")
    parimelazhagar_explanations = {}
    if os.path.exists('krl.db'):
        conn_krl = sqlite3.connect('krl.db')
        cursor_krl = conn_krl.cursor()
        cursor_krl.execute("SELECT kural_id, translation FROM urai WHERE a_id = 29")
        for row in cursor_krl.fetchall():
            parimelazhagar_explanations[row[0]] = row[1]
        conn_krl.close()
    else:
        print("Warning: krl.db not found. Parimelazhagar's explanations will be empty.")

    # Create the new database
    print("Creating thirukkural.db...")
    conn = sqlite3.connect('thirukkural.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS thirukkural (
            id INTEGER PRIMARY KEY,
            kural_line1 TEXT,
            kural_line2 TEXT,
            iyal TEXT,
            athigaaram TEXT,
            translation TEXT,
            explanation_mv TEXT,
            explanation_sp TEXT,
            explanation_mk TEXT,
            explanation_parimelazhagar TEXT
        )
    ''')

    # Insert data
    for kural in kurals_data:
        k_id = kural['Number']
        line1 = kural['Line1']
        line2 = kural['Line2']
        translation = kural['Translation']
        mv = kural['mv']
        sp = kural['sp']
        mk = kural['mk']
        
        meta = kural_meta.get(k_id, {'iyal': '', 'athigaaram': ''})
        iyal = meta['iyal']
        athigaaram = meta['athigaaram']
        
        parimelazhagar = parimelazhagar_explanations.get(k_id, '')

        cursor.execute('''
            INSERT INTO thirukkural (
                id, kural_line1, kural_line2, iyal, athigaaram, translation,
                explanation_mv, explanation_sp, explanation_mk, explanation_parimelazhagar
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (k_id, line1, line2, iyal, athigaaram, translation, mv, sp, mk, parimelazhagar))

    conn.commit()
    conn.close()
    print("Database thirukkural.db created successfully with 1330 kurals!")

if __name__ == '__main__':
    main()
