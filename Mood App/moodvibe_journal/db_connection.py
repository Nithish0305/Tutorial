import psycopg2

# Database config
DB_NAME = "MoodApp"
DB_USER = "postgres"
DB_PASSWORD = "postgres"   # your password
DB_HOST = "localhost"
DB_PORT = "5432"

def get_db_connection():
    """Get a connection to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Database connection established successfully")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return None

def test_connection():
    """Test the database connection and print table information"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        # Example 1: Fetch all songs
        cur.execute("SELECT song_id, mood, file_path FROM journal_songs;")
        songs = cur.fetchall()
        print("Songs:")
        for s in songs:
            print(s)
        
        # Example 2: Fetch all quotes
        cur.execute("SELECT quote_id, mood, quote FROM journal_quotes;")
        quotes = cur.fetchall()
        print("\nQuotes:")
        for q in quotes:
            print(q)
        
        # Example 3: Fetch journal history (with JOINs)
        cur.execute("""
            SELECT j.journal_id, j.username, j.mood, j.request_time,
                   s.file_path, q.quote
            FROM journal_journal j
            LEFT JOIN journal_songs s ON j.song_id = s.song_id
            LEFT JOIN journal_quotes q ON j.quote_id = q.quote_id
            ORDER BY j.request_time DESC;
        """)
        journal_entries = cur.fetchall()
        print("\nJournal History:")
        for entry in journal_entries:
            print(entry)
        
        # Cleanup
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error testing database: {str(e)}")
        if conn:
            conn.close()
        return False

def insert_journal_entry(username, mood, song_id, quote_id):
    """Insert a new journal entry using direct PostgreSQL connection"""
    conn = get_db_connection()
    if not conn:
        print("Failed to get database connection")
        return None
    
    try:
        cur = conn.cursor()
        print(f"Inserting journal entry: username={username}, mood={mood}, song_id={song_id}, quote_id={quote_id}")
        cur.execute("""
            INSERT INTO journal_journal (username, mood, song_id, quote_id, request_time)
            VALUES (%s, %s, %s, %s, NOW())
            RETURNING journal_id;
        """, (username, mood, song_id, quote_id))
        
        journal_id = cur.fetchone()[0]
        conn.commit()
        print(f"Journal entry inserted with ID: {journal_id}")
        return journal_id
    except Exception as e:
        conn.rollback()
        print(f"Error inserting journal entry: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        conn.close()

# Run test if this script is executed directly
if __name__ == "__main__":
    test_connection()