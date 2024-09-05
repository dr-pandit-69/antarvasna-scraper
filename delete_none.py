import sqlite3

def delete_entries_with_string_none():

    conn = sqlite3.connect('comic_data.db')
    cursor = conn.cursor()

    try:
       
        cursor.execute('''
            DELETE FROM comic_data
            WHERE post_title = 'None'
            OR english_title = 'None'
            OR author = 'None'
            OR date = 'None'
            OR likes = 'None'
            OR dislikes = 'None'
            OR story_content = 'None'
            OR url = 'None'
        ''')

    
        conn.commit()
        print(f"Entries with the text 'None' have been deleted.")

    except sqlite3.Error as e:
        print(f"Failed to delete entries: {e}")

    finally:
       
        conn.close()

if __name__ == "__main__":
    delete_entries_with_string_none()
