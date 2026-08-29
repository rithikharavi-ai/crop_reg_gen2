import json
import psycopg2

conn = psycopg2.connect(dbname="cropsown", user="postgres", password="password", host="localhost", port="5432")
cur = conn.cursor()
cur.execute("SELECT section_ui_schema FROM g2p_register_sections WHERE section_id = 'cropsown_cropsown_record_section_01'")
row = cur.fetchone()
if row:
    schema = row[0]
    with open('schema_dump.json', 'w') as f:
        json.dump(schema, f, indent=2)
    print("Schema dumped to schema_dump.json")
else:
    print("Schema not found")
