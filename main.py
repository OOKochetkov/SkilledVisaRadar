import requests
from bs4 import BeautifulSoup
import hashlib
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from openai import OpenAI
import os
from dotenv import load_dotenv

# ========== LOAD ENV ==========
# Path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

URLS = os.getenv("URLS").split(",")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 3600))
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASS = os.getenv("EMAIL_PASS")

last_hashes = {}

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ========== FUNCTIONS ==========
def summarize_change(text):
    """Send changed text to GPT for summarization."""
    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=[
                {"role": "developer", "content": "You help to analyse skilled migration website. Summarize updates about Australian visa programs (only skilled visa 190 and 491) clearly and concisely."},
                {"role": "user", "content": text}
            ],
            max_output_tokens=700
        )
        return response.output_text.strip()
    
    except Exception as e:
        return f"(AI summary failed: {e})\n\n{text}"

def send_alert(subject, body):
    """Send email alert with update summary."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)

def check_page(url):
    """Fetch page, detect change, summarize if needed."""
    global last_hashes
    response = requests.get(url, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract visible text (headings + paragraphs)
    keywords = ["190", "491", "skilled visa", "state nominated"]
    text_content = "\n".join([
        t.get_text(strip=True)
        for t in soup.find_all(["h1","h2","h3","p","li"])
        if any(k.lower() in t.get_text(strip=True).lower() for k in keywords)
    ])
    
    current_hash = hashlib.sha256(text_content.encode()).hexdigest()

    if url in last_hashes and current_hash != last_hashes[url]:
        summary = summarize_change(text_content)
        send_alert("Visa Program Update Detected", f"🔔 Change found on {url}\n\n+++JUNIOR AI ASSISTANT REPORTS+++\n{summary}")

    last_hashes[url] = current_hash

# ========== MAIN LOOP ==========
if __name__ == "__main__":
    t = 0
    while True:
        for url in URLS:
            t += 1
            try:
                check_page(url)
            except Exception as e:
                print(f"Error checking {url}: {e}")
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Heartbeat: total checks = {t} | Last check at {now}")
        
        time.sleep(CHECK_INTERVAL)
       


