import sqlite3


def init_db():
    conn = sqlite3.connect('comic_data.db')  
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comic_data (
        url TEXT PRIMARY KEY,
        post_title TEXT,
        english_title TEXT,
        author TEXT,
        date TEXT,
        likes INTEGER,
        dislikes INTEGER,
        story_content TEXT
    )
    ''')

    conn.commit()
    conn.close()

if __name__=='__main__':

    init_db()
