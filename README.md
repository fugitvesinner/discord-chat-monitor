# Discord Message Logger

> A Discord bot that logs deleted and edited messages to a webhook with formatted embeds.

## Features
- Logs deleted messages with attachments
- Logs edited messages showing before/after content
- Offline status for stealth operation
- Colored console logging
- File logging
- Webhook integration with user avatars

## Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/discord-message-logger.git
cd discord-message-logger 
```

2. **Install requirements**
- pip install -r requirements.txt

3. **Configure the bot**

```json
{
    "server_id": "YOUR_SERVER_ID",
    "token": "YOUR_BOT_TOKEN",
    "webhook": "YOUR_WEBHOOK_URL"
}
```

4. **Get credentials**

- Create a bot in Discord Developer Portal
- Enable Message Content Intent in bot settings
- Invite bot to your server with necessary permissions
- Create a webhook in your server channel settings


## Project Structure
```
discord-chat-monitor/
├── main.py
├── config.json
├── requirements.txt
├── utils/
│   └── log.py
└── bot.log (created automatically)
```

## Permissions Needed

- View Channels
- Read Message History
- Send Messages (for webhook)
- Manage Webhooks

<div align="center">
⭐ Star this repository if you find it helpful!
</div>