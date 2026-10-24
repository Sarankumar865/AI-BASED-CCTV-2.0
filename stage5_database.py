import sqlite3
from datetime import datetime

# Create or open the database file
connection = sqlite3.connect("cctv_events.db")
cursor = connection.cursor()

# Create the event history table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_time TEXT NOT NULL,
        event_type TEXT NOT NULL,
        description TEXT NOT NULL
    )
""")

# Save a sample event
event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cursor.execute(
    "INSERT INTO events (event_time, event_type, description) VALUES (?, ?, ?)",
    (
        event_time,
        "TEST",
        "AI CCTV database test successful"
    )
)

connection.commit()

# Display saved events
print("AI CCTV 2.0 - Event History")
print("-" * 50)

cursor.execute(
    "SELECT id, event_time, event_type, description FROM events ORDER BY id DESC"
)

for event in cursor.fetchall():
    print(event)

connection.close()

print("\nDatabase test completed!")
print("Check cctv_events.db in your project folder.")