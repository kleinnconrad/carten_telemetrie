import feedparser
from bs4 import BeautifulSoup
import os
from datetime import datetime

POST_ID = '1s9dydh'
# Die URL mit .rss am Ende
RSS_URL = f'https://www.reddit.com/r/esp32/comments/{POST_ID}/.rss'

# Einen eigenen User-Agent setzen, damit Reddit uns nicht blockiert
USER_AGENT = 'GitHubAction:carten-telemetry-rss-sync:v1.0'

print(f"Lese RSS Feed: {RSS_URL}")
feed = feedparser.parse(RSS_URL, agent=USER_AGENT)

if feed.bozo: # bozo = 1 bedeutet, dass es einen Fehler beim Parsen gab (z.B. Blockade)
    print("Fehler beim Abrufen des Feeds!")
    exit(1)

# Markdown Header zusammenbauen
md_content = "# Reddit Feedback: Live Telemetry System (RSS Sync)\n\n"
md_content += f"**Letzter Sync:** {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
md_content += "---\n\n"

# Durch die Einträge iterieren. Der erste Eintrag ist oft der Post selbst, danach die Kommentare.
for entry in feed.entries:
    # Autor auslesen (Reddit formatiert das als /u/username)
    author = entry.get('author', '[Unbekannt]').replace('/u/', '')
    link = entry.get('link', '')
    
    # Der eigentliche Text steckt als HTML in der "summary"
    raw_html = entry.get('summary', '')
    
    # BeautifulSoup nutzen, um HTML-Tags (wie <p>, <a>) zu entfernen
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # Text extrahieren und Zeilenumbrüche beibehalten
    text = soup.get_text(separator='\n').strip()
    
    # Markdown Blockquote Formatierung hinzufügen (> )
    text_formatted = text.replace('\n', '\n> ')
    
    md_content += f"**u/{author}** [schrieb]({link}):\n"
    md_content += f"> {text_formatted}\n\n"
    md_content += "---\n\n"

# Zielordner erstellen und speichern
os.makedirs('reddit', exist_ok=True)
file_path = 'reddit/reddit_feedback.md'

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(md_content)
    
print(f"Erfolgreich {len(feed.entries)} Einträge in {file_path} gespeichert!")
