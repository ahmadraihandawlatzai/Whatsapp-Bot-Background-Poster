import os
import sqlite3
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

print("⌨️ [USER INPUT REQUIRED]: Please enter your marketing message below.")
print("👉 Note: You can paste multiline text. To finish and launch the bot, press Ctrl+D (on Linux) or type 'END' on a clean line and press Enter:")

user_lines = []
while True:
    try:
        line = input()
        if line.strip() == "END": 
            break
        user_lines.append(line)
    except EOFError: 
        break
        
sample_message = "\n".join(user_lines)

if not sample_message.strip():
    print("❌ [ERROR]: Message body cannot be empty! System shutting down.")
    quit()

print("✅ [PAYLOAD SECURED]: Dynamic message locked successfully into local system memory!")

print("🌐 [SELENIUM Engine]: Awakening automated Chrome console...")

chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={os.getcwd()}/whatsapp_session")
driver = webdriver.Chrome(options=chrome_options) 
driver.get("https://web.whatsapp.com") 

print("📸 [ACTION REQUIRED]: Scan the QR Code ONCE. (Skip if already logged in)")
time.sleep(160) 

conn = sqlite3.connect('whatsapp.sqlite')
cur = conn.cursor()

if not os.path.exists('whatsapp.sqlite') or os.path.getsize('whatsapp.sqlite') < 100:
    print("⚙️ [DATABASE]: Provisioning fresh tables...")
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
    sample_groups = [
        ("Alsudais Travel Agency", "alsudais_real_channel")
    ]
    for name, g_id in sample_groups:
        cur.execute('INSERT OR IGNORE INTO whatsapp_groups (group_name, group_id) VALUES (?, ?)', (name, g_id))

    cur.execute('INSERT INTO messages_queue (message_text) VALUES (?)', (sample_message,))
    conn.commit()
    print("✅ [DATABASE]: Relational schema deployment complete.")

try:
    while True:
        print("\n📡 [BACKGROUND WORKER]: Scanning database for pending payloads...")
        conn = sqlite3.connect('whatsapp.sqlite')
        cur = conn.cursor()
        cur.execute("SELECT id, message_text FROM messages_queue WHERE status = 'PENDING'")
        message_row = cur.fetchone()

        if message_row is None:
            print("💤 [WORKER]: No pending messages found in queue. Re-scanning in 15 minutes...")
            cur.close()
            conn.close()
            time.sleep(900) 
            continue 

        message_id = message_row[0]
        target_message = message_row[1]

        print(f"🎯 [FOUND]: Message ID [{message_id}] locked and ready for delivery!")
        print(f"📝 [PAYLOAD]: '{target_message}'")

        print("\n📋 [GROUPS FETCH]: Extracting target distribution channels...")
        cur.execute("SELECT group_name, group_id FROM whatsapp_groups")

    
        for name, g_id in cur:
            print(f"\n🚀 Attempting live delivery to group: {name}")
        
            try:
            
                actions = ActionChains(driver)
                actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys("/").key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
                time.sleep(2) 
            
                actions.send_keys(Keys.CONTROL + "a").send_keys(Keys.BACKSPACE).perform()
                time.sleep(1)
                actions.send_keys(name).perform()
                print(f"⌨️ [KEYBOARD SIMULATION]: Successfully typed group name: '{name}'")
                time.sleep(4) 
            
                actions.send_keys(Keys.ENTER).perform()
                print("🔓 [CHAT OPENED]: Successfully entered the conversation window!")
                time.sleep(4) 
            
                actions.send_keys(Keys.ENTER).perform()
                print("🔓 [CHAT OPENED]: Successfully entered the conversation window!")
                time.sleep(4) 
                
                message_lines = target_message.split('\n')
                for index, line in enumerate(message_lines):
                    actions.send_keys(line).perform()
                    if index < len(message_lines) - 1:
                        actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                        time.sleep(0.2)
            
                actions.send_keys(Keys.ENTER).perform()
                print(f"✅ [TRANSMITTED]: Cohesive multiline block successfully posted to: {name}")
            
            except Exception as web_error:
                print(f"⚠️ [STEALTH ERROR]: Execution failed for {name}. Details: {web_error}")

            random_delay = random.randint(4, 8)
            print(f"⏳ [ANTI-BAN]: Freezing system for {random_delay} seconds...")
            time.sleep(random_delay)

        cur.close()
        conn.close()
        print("🏁 [CYCLE COMPLETE]: All target groups processed successfully.")
    
        print("⏰ [TIMER]: Entering deep sleep for 15 minutes (900 seconds) before next run...")
        time.sleep(900) 
except KeyboardInterrupt:
    print("\n🛑 [SHUTTING DOWN]: Exit signal received from keyboard. Terminating background operations safely...")
    try:
        cur.close()
        conn.close()
    except:
        pass 
    driver.quit() 
    print("🔒 [STATUS]: Database streams disengaged and Chrome session locked. Goodbye!")
