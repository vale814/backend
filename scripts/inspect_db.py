import sqlite3
p = r"C:\Users\Karen Ariza\Desktop\backend\lindeza.db"
try:
    conn = sqlite3.connect(p)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(producto)")
    rows = cur.fetchall()
    if not rows:
        print('No table producto found')
    else:
        for r in rows:
            print(r)
    conn.close()
except Exception as e:
    print('ERROR', e)
