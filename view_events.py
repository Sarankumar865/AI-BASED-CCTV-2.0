import sqlite3

connection = sqlite3.connect("cctv_events.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT id, event_time, event_type, description
    FROM events
    ORDER BY id DESC
""")

events = cursor.fetchall()

print("\nAI CCTV 2.0 - SAVED EVENT HISTORY")
print("-" * 70)

if not events:
    print("No events recorded.")
else:
    for event in events:
        print(
            f"ID: {event[0]}\n"
            f"Time: {event[1]}\n"
            f"Type: {event[2]}\n"
            f"Description: {event[3]}\n"
            + "-" * 70
        )

connection.close()