# 📋 BriefBot — AI-Powered Candidate Summary Bot

BriefBot is an automation assistant that pulls candidate data from Airtable, summarizes it using OpenAI, and posts a clean, categorized report into a Slack channel — perfect for busy recruiters and hiring teams.

## 🚀 Features

* 🧠 Summarizes new candidates, missed interviews, follow-ups, and top fits
* 🔗 Connects Airtable → OpenAI → Slack
* 💬 Delivers summaries straight into Slack
* 🌱 Lightweight, fast, free (OpenAI pay-as-you-go)

## ⚙️ Setup Instructions

### ✅ 1. Clone this Repo

```bash
git clone https://github.com/megasxgigavolt/BriefBot-AI-Agent.git
cd briefbot
```

### ✅ 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### ✅ 3. Set Up Airtable

* Get your Airtable API Key: [https://airtable.com/account](https://airtable.com/account)
* Visit [https://airtable.com/api](https://airtable.com/api) to find your:

  * **Base ID** (starts with `app...`)
  * **Table name** (e.g. `Candidates`)
  * <img width="1308" height="545" alt="image" src="https://github.com/user-attachments/assets/5ce77035-92ed-4830-b45d-88e09d6cb50c" />


### ✅ 4. Get OpenAI API Key

* Visit: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
* Create a secret key that starts with `sk-...`
  ❌ Don’t use `sk-proj` or `proj-` keys

### ✅ 5. Create a Slack Bot

* Go to: [https://api.slack.com/apps](https://api.slack.com/apps)
* Click **Create New App → From Scratch**
* Name it: `BriefBot`, choose your workspace
* Go to **OAuth & Permissions**
* Add the following **Bot Token Scopes**:

  * `chat:write`
  * `channels:read`
  * `groups:read` (for private channels)
* Click **Install to Workspace** and copy your **Bot Token** (`xoxb-...`)
* In Slack, invite your bot to a channel:

  ```bash
  /invite @BriefBot
  ```

### ✅ 6. Create a `.env` File

In the root directory, create a file called `.env`:

```env
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=appXXXXXXXXXXXX
AIRTABLE_TABLE_NAME=Candidates
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_CHANNEL=#briefbot-updates
```

### ✅ 7. Run BriefBot

```bash
python briefbot.py
```

You’ll see a Slack message appear in your selected channel with a summary of candidate activity.

## 💡 Pro Tips

* Adjust temperature in the script for more creative vs. deterministic output
* Filter by view or date inside Airtable to limit the data
* Use `cron` or GitHub Actions for daily runs (ask us how!)

## 📄 License

MIT License

## 🙌 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to improve.
