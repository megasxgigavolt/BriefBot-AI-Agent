import os
import requests
import openai
from datetime import datetime
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# ----------------------------------------
# 🔐 Load environment variables from .env
# ----------------------------------------
load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")

# ----------------------------------------
# 📡 Airtable Configuration
# ----------------------------------------
AIRTABLE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

# ----------------------------------------
# 🔎 Step 1: Fetch Candidate Records
# ----------------------------------------
def fetch_candidates():
    params = {
        "pageSize": 100,
        "view": "Grid view"  # Change to a specific Airtable view if needed
    }
    response = requests.get(AIRTABLE_URL, headers=HEADERS, params=params)
    records = response.json().get("records", [])
    return records

# ----------------------------------------
# 🧹 Step 2: Format Candidate Records
# ----------------------------------------
def format_candidates(records):
    output = []
    for record in records:
        fields = record.get("fields", {})
        name = fields.get("Name", "Unnamed")
        job = fields.get("Job Applied For", "Unknown Role")
        status = fields.get("Status", "No Status")
        interview = fields.get("Interview Date", "N/A")
        fit = fields.get("Fit Score", "N/A")
        output.append(f"- {name} | {job} | Status: {status} | Interview: {interview} | Fit Score: {fit}")
    return "\n".join(output)

# ----------------------------------------
# 🤖 Step 3: Generate Summary via OpenAI
# ----------------------------------------
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_summary(candidate_text):
    prompt = f"""
You are BriefBot, a helpful recruitment assistant.

Summarize the following candidate activity. Categorize them into:
- New Applicants (just mention the top 5 names)
- Missed Interviews (compare with today's date to determine if missed)
- Follow-ups Needed
- Top Fit Candidates

Here is the data:
{candidate_text}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are BriefBot, a helpful recruitment assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.1
    )
    return response.choices[0].message.content

# ----------------------------------------
# 💬 Step 4: Send Summary to Slack
# ----------------------------------------
slack_client = WebClient(token=SLACK_TOKEN)

def post_to_slack(message):
    try:
        slack_client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message
        )
        print("✅ Sent to Slack!")
    except SlackApiError as e:
        print(f"❌ Slack Error: {e.response['error']}")

# ----------------------------------------
# 🚀 Run BriefBot
# ----------------------------------------
if __name__ == "__main__":
    records = fetch_candidates()
    if not records:
        print("No records found.")
    else:
        candidate_text = format_candidates(records)
        summary = generate_summary(candidate_text)
        post_to_slack(f"📋 *BriefBot Summary – {datetime.now().strftime('%B %d')}*\n\n{summary}")
