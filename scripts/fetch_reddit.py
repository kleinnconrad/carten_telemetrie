import requests
import json
from datetime import datetime
import os

# Die ID deines Posts aus der URL
POST_ID = '1s9dydh'
URL = f'https://www.reddit.com/r/esp32/comments/{POST_ID}.json'

# Reddit blockiert Standard-Python-Requests. Ein Custom User-Agent ist Pflicht.
headers = {'User-Agent': 'GitHubAction:carten-telemetry-feedback:v1.0'}

response = requests.get(URL, headers=headers)
if response.status_code != 200:
    print(f"Fehler beim Abrufen der Reddit API: {response.status_code}")
    exit(1)

data = response.json()

# Extrahieren der Post-Metadaten und der Kommentare
post_data = data[0]['data']['children'][0]['data']
comments_data = data[1]['data']['children']

# Markdown Header zusammenbauen
md_content = "# Reddit Feedback: Live Telemetry System\n\n"
md_content += f"**Original Post:** [{post_data['title']}](https://www.reddit.com{post_data['permalink']})\n"
md_content += f"**Letzter Sync:** {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
md_content += "---\n\n"

# Funktion, um Kommentare und deren Threads rekursiv zu parsen
def extract_comments(comments_list, depth=0):
    content = ""
    for item in comments_list:
        # "load more comments" Platzhalter ignorieren
        if item['kind'] == 'more':
            continue
            
        comment = item['data']
        author = comment.get('author', '[deleted]')
        body = comment.get('body', '')
        permalink = comment.get('permalink', '')
        
        # Replies visuell durch Zitat-Blöcke einrücken
        indent = "> " * (depth + 1)
        body_formatted = body.replace('\n', f'\n{indent}')
        
        content += f"**u/{author}** [schrieb](https://www.reddit.com{permalink}):\n"
        content += f"{indent}{body_formatted}\n\n"
        
        # Wenn der Kommentar weitere Antworten hat, rufe die Funktion rekursiv auf
        if 'replies' in comment and comment['replies'] != '':
            content += extract_comments(comment['replies']['data']['children'], depth + 1)
            
    return content

md_content += extract_comments(comments_data)

# Zielordner erstellen, falls er noch nicht existiert
os.makedirs('docs', exist_ok=True)

# Markdown Datei schreiben
file_path = 'docs/reddit_feedback.md'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(md_content)
    
print(f"Erfolgreich in {file_path} gespeichert!")
