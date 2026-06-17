import json
import os
from datetime import datetime
import requests

# 1. Load the schedule
# Replace 'schedule.json' with the exact filename of your JSON file in GitHub
with open('schedule.json', 'r') as file:
    data = json.load(file)

# 2. Get today's date formatted to match your JSON (e.g., "Wednesday, June 17")
today_str = datetime.now().strftime("%A, %B %d").replace(" 0", " ")
# Quick fallback check: strip any trailing whitespaces in your JSON comparison data
todays_events = [e for e in data['schedule'] if e['georgian_date'].strip() == today_str]

if not todays_events:
    print(f"No events found for today ({today_str}). Exiting script.")
    exit(0)

# 3. Construct the WhatsApp Card Layout
islamic_date = todays_events[0]['islamic_date'] # Grab Islamic date from first entry

card =  "============================\n"
card += "🕋 *TODAY'S ISLAMIC EVENTS* 🕋\n"
card += "============================\n"
card += f"📅 *Date:* {today_str} ({islamic_date})\n\n"

for index, event in enumerate(todays_events, start=1):
    speaker_title = "Zakira" if event['type'] == "Ladies" else "Maulana"
    sponsor = event['sponsors'].strip() if event['sponsors'].strip() else "Open"
    
    card += "----------------------------\n"
    card += f"📢 *PROGRAM {index}: {event['type'].upper()}'S MAJLIS*\n"
    card += "----------------------------\n"
    card += f"🔹 *Event:* {event['event']}\n"
    card += f"⏰ *Time:* {event['time']}\n"
    card += f"🎙️ *{speaker_title}:* {event['maulana']}\n"
    card += f"🤝 *Sponsor:* {sponsor}\n"
    card += f"📍 *Address:* {event['address']}\n\n"

card += "_Please join on time. Elteyas-e-Dua._\n"
card += "============================"

print("Generated Card Layout:\n", card)

# 4. Send Message via WhatsApp API
# Example using Cloud API / Twilio Sandbox config
WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN')
RECIPIENT_DATA = os.environ.get('WHATSAPP_RECIPIENT_ID') # Group ID or Phone Number

# Note: Adjust payload structures depending on your provider (Twilio vs Meta Native Business API)
url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_DATA,
    "type": "text",
    "text": {
        "preview_url": False,
        "body": card
    }
}

response = requests.post(url, headers=headers, json=payload)
print("Status Code:", response.status_code)
print("Response:", response.text)
