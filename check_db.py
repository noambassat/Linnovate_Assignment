import os
import psycopg2

def view_highlights():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "highlights_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres")
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT video_id, segment_path, timestamp, description, llm_summary
            FROM highlights
            ORDER BY video_id, timestamp
            LIMIT 10;
        """)
        rows = cur.fetchall()

        if not rows:
            print("No highlights found.")
        else:
            for row in rows:
                print(f"\nVideo ID: {row[0]}")
                print(f"Segment:  {row[1]}")
                print(f"Time:     {row[2]}")
                print(f"Description: {row[3]}")
                print(f"Summary:     {row[4]}")

        cur.close()
        conn.close()
    except Exception as e:
        print("Error reading from database:", e)

if __name__ == "__main__":
    view_highlights()
