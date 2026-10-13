# General Purpose WhatsApp Automated Group Poster

This is a Python-based background automation script that allows you to input a single marketing or informational message in your terminal and automatically broadcast it to a list of target groups saved in a local database. The bot runs continuously on an infinite loop, sending the message to all targets and then waiting for 15 minutes before repeating the process.

To prevent WhatsApp Web layout changes from breaking the script, it completely avoids looking for fragile CSS classes or XPath locators on the page. Instead, it uses virtual keyboard actions and official shortcuts to navigate the search bar and the message box.

## Key Features
* Dynamic Terminal Input: You can paste any long, multiline text block directly into the terminal at runtime, complete with emojis and links.
* Session Memory: The Chrome browser uses a dedicated user-data folder to save session cookies. This means you only need to link your WhatsApp phone via the QR code the very first time you launch the application.
* Single-Message Formatting: The script automatically breaks down multiline input strings and stitches them back together in the chat window using Shift+Enter actions so your long posts are delivered as one cohesive message instead of separate spammy lines.
* Human Delay Simulation: It pauses randomly for a few seconds between different groups so that the sending pattern looks organic rather than mechanical.
* Safe Interrupt Handler: Wrapping the master tracking loop inside a standard system keyboard exception allows you to close the application immediately using Ctrl+C without corrupting your data or crashing the chrome browser environment.

## Database Layout (whatsapp.sqlite)
The script relies on a local relational SQLite database consisting of two simple tables:
1. `whatsapp_groups`: Stores the target group name identifiers that the browser types into the lookup console.
2. `messages_queue`: Keeps track of the raw text string message payload that you feed into the runtime parser.

## How to Set It Up and Run It

1. Prepare your local environment by installing the Selenium package in your terminal:
pip install selenium --break-system-packages

2. Make sure your workspace directory structure matches this layout:
AI- JOURNEY/
└── whatsapp bot/
    ├── whatsapp bot.py
    └── whatsapp_session/ (This folder is generated automatically to store your login data)

3. Update the `sample_groups` list inside the database section of your `whatsapp bot.py` file with the exact visual names of the WhatsApp groups you want to target.

4. Open your terminal and run the main application:
python3 "whatsapp bot.py"

5. Provide your text payload:
* The terminal will ask you to enter your message.
* Paste or type your text.
* Move to a fresh line, type END, and press Enter to lock the message and start the web automation browser.

6. To stop the continuous script at any point during its execution or while it is waiting in deep sleep, just go back to your terminal and hit:
Ctrl + C
