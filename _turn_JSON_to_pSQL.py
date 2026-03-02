import psycopg2
import json

# Database connection
conn = psycopg2.connect(database="42bot_data", user="postgres", password="1337")
cur = conn.cursor()

# First, drop the tables if they exist (in correct order due to foreign key)
cur.execute("DROP TABLE IF EXISTS video_snapshots CASCADE;")
cur.execute("DROP TABLE IF EXISTS videos CASCADE;")

# Create videos table
cur.execute(
    """
    CREATE TABLE videos (
        id VARCHAR(36) PRIMARY KEY,
        creator_id VARCHAR(36) NOT NULL,
        video_created_at TIMESTAMP WITH TIME ZONE NOT NULL,
        views_count INTEGER NOT NULL,
        likes_count INTEGER NOT NULL,
        comments_count INTEGER NOT NULL,
        reports_count INTEGER NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL
    );
    """
)

# Create video_snapshots table
cur.execute(
    """
    CREATE TABLE video_snapshots (
        id VARCHAR(36) PRIMARY KEY,
        video_id VARCHAR(36) NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
        views_count INTEGER NOT NULL,
        likes_count INTEGER NOT NULL,
        comments_count INTEGER NOT NULL,
        reports_count INTEGER NOT NULL,
        delta_views_count INTEGER NOT NULL,
        delta_likes_count INTEGER NOT NULL,
        delta_comments_count INTEGER NOT NULL,
        delta_reports_count INTEGER NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL
    );
    """
)

# Read and parse JSON file
try:
    with open('videos.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: videos.json file not found!")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    exit(1)

# Insert videos and their snapshots
videos_inserted = 0
snapshots_inserted = 0

for video in data['videos']:
    # Insert video
    cur.execute(
        """
        INSERT INTO videos 
        (id, creator_id, video_created_at, views_count, likes_count, 
         comments_count, reports_count, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            video['id'],
            video['creator_id'],
            video['video_created_at'],
            video['views_count'],
            video['likes_count'],
            video['comments_count'],
            video['reports_count'],
            video['created_at'],
            video['updated_at']
        )
    )
    videos_inserted += 1
    
    # Insert snapshots for this video
    for snapshot in video['snapshots']:
        cur.execute(
            """
            INSERT INTO video_snapshots 
            (id, video_id, views_count, likes_count, comments_count, 
             reports_count, delta_views_count, delta_likes_count, 
             delta_comments_count, delta_reports_count, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                snapshot['id'],
                snapshot['video_id'],
                snapshot['views_count'],
                snapshot['likes_count'],
                snapshot['comments_count'],
                snapshot['reports_count'],
                snapshot['delta_views_count'],
                snapshot['delta_likes_count'],
                snapshot['delta_comments_count'],
                snapshot['delta_reports_count'],
                snapshot['created_at'],
                snapshot['updated_at']
            )
        )
        snapshots_inserted += 1

# Commit the transaction
conn.commit()

print(f"Successfully inserted:")
print(f"  - {videos_inserted} videos")
print(f"  - {snapshots_inserted} snapshots")

# Optional: Show some statistics
cur.execute("SELECT COUNT(*) FROM videos")
video_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM video_snapshots")
snapshot_count = cur.fetchone()[0]

print(f"\nFinal counts in database:")
print(f"  - Videos: {video_count}")
print(f"  - Snapshots: {snapshot_count}")

# Close connection
cur.close()
conn.close()