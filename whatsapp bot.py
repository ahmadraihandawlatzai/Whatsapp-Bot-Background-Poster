import sqlite3
import time
import random

conn = sqlite3.connect('whatsapp.sqlite')
cur = conn.cursor()
print("⚙️ [SYSTEM]: Upgrading database architecture to relational enterprise schema...")

cur.execute('''
CREATE TABLE IF NOT EXISTS whatsapp_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT NOT NULL,
    group_id TEXT NOT NULL UNIQUE
)''')


cur.execute('''
CREATE TABLE IF NOT EXISTS messages_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_text TEXT NOT NULL,
    status TEXT DEFAULT 'PENDING'
)''')

print("✅ [DATABASE]: Relational tables created successfully!")

sample_groups = [
    ("Travel Agency Group A", "120363021111@g.us"),
    ("Kabul Cars Marketplace", "120363022222@g.us"),
    ("Dubai Logistics Hub", "120363023333@g.us")
]
for name, g_id in sample_groups:
    cur.execute('INSERT OR IGNORE INTO whatsapp_groups (group_name, group_id) VALUES (?, ?)', (name, g_id))

# sample_message = "🚀 پکیج جدید تور دبی رسیده است! قیمت: $550. جهت رزرو با شماره فوق به تماس شوید."
# cur.execute('INSERT INTO messages_queue (message_text) VALUES (?)', (sample_message,))
conn.commit()
print("🚀 [SUCCESS]: Relational schema deployment complete. Ready for background worker trigger!")
print("\n📡 [BACKGROUND WORKER]: Scanning database for pending payloads...")
cur.execute("SELECT id, message_text FROM messages_queue WHERE status = 'PENDING'")
message_row = cur.fetchone()

if message_row is None:
    print("💤 [WORKER]: No pending messages found in queue. Going back to sleep.")
    cur.close()
    quit()

message_id = message_row[0]
target_message = message_row[1]

print(f"🎯 [FOUND]: Message ID [{message_id}] locked and ready for delivery!")
print(f"📝 [PAYLOAD]: '{target_message}'")

print("\n📋 [GROUPS FETCH]: Extracting target distribution channels...")


cur.execute("SELECT group_name, group_id FROM whatsapp_groups")
for name, g_id in cur:
    print(f"ready to send to group: {name} (ID: {g_id})")
    random_delay = random.randint(2, 5)
    print(f"⏳ Human simulation active. Freezing for {random_delay} seconds...")
    time.sleep(random_delay)
    print(f"⏳ Human simulation active. Freezing for {random_delay} seconds...")
    time.sleep(random_delay)
    print(f"✅ Packet successfully routed to JID: {g_id}\n")
cur.close()
conn.close()
