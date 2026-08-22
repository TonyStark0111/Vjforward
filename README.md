# Xeon Forward Bot v5 – Multi-Bot Edition

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com/?lines=Welcome+To+Xeon+Forward+Bot+!&center=true&width=380&height=45">
</p>

---

## 🔥 New in v5

- **Multi-Bot Support** – Add up to **3 bots + 1 userbot** (total 4 forwarding identities)
- **Bot Selection** – Choose which bot to use for each forward via inline buttons
- **Per-Bot Settings** – Each bot has its own caption, button, filters, extra settings, and turbo mode
- **No User Lock** – Multiple users can forward simultaneously
- **Per-Bot Locking** – Each bot can run only one forward at a time; other bots remain free
- **Smart Channel Access** – Tries the selected bot first; falls back to userbot only if needed
- **Improved Private Channel Support** – Works seamlessly when your bot is an admin

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Public Forward** | Forward messages from any public channel |
| **Private Forward** | Forward from private channels using your userbot |
| **Custom Caption** | Add your own caption with `{filename}`, `{size}`, `{caption}` |
| **Custom Button** | Add inline buttons to forwarded messages |
| **Skip Duplicate** | Avoid forwarding duplicate media (uses MongoDB) |
| **Skip by Extensions** | Exclude files with specific extensions (e.g., .mp4, .exe) |
| **Skip by Keywords** | Only forward messages containing exact keywords |
| **Filter by Media Type** | Choose which media types to forward (docs, videos, photos, etc.) |
| **Size Limit** | Set minimum and maximum file size |
| **Link Removal** | Automatically remove all URLs and mentions from captions |
| **Replacement Link** | Replace all URLs/mentions with a Telegram username or custom URL |
| **HTML Tag Cleaning** | Removes anchor tags like `<a href="...">...</a>` automatically |
| **Forward Delay** | Custom delay between forwarded messages (0 = auto based on bot type) |
| **Turbo Mode** | Set a count of messages after which the bot sleeps, and specify sleep duration |
| **Auto-Restart** | Pending forwards resume automatically after bot restart |
| **Per-User Settings** | All settings are stored per user in the database |
| **Batch Optimization** | Automatically switches to individual copying when link modifications are enabled |

---

## ⚙️ Commands

| Command | Description |
|---------|-------------|
| `/start` | Check if I'm alive |
| `/forward` | Start a new forward |
| `/unequify` | Delete duplicate media messages in a chat |
| `/settings` | Open settings panel (manage bots, channels, per-bot configs) |
| `/stop` | Stop your ongoing forward |
| `/reset` | Reset your settings to default |
| `/restart` | Restart the server (owner only) |
| `/resetall` | Reset all users' settings (owner only) |
| `/broadcast` | Broadcast a message to all users (owner only) |

---

## 📋 How to Use

### 1. Add Your Bots
- Go to `/settings` → **Bots** → Add Bot / Add Userbot
- You can add up to **3 bot tokens** and **1 userbot session**
- Each bot must be enabled (toggle ON)

### 2. Add Target Channels
- Go to `/settings` → **Channels** → Add Channel
- Your bot/userbot must be an **admin** in the target channel

### 3. Start Forwarding
- Use `/forward` command
- If you have multiple bots, you'll be asked which one to use
- Provide the source chat (link or forwarded message)
- Select target channel and skip number
- Confirm and the forward will begin

### 4. Customize Each Bot
- Each bot has its own settings:
  - Caption, Button, Filters
  - Size limits, Keywords, Extensions
  - Link removal, Replacement link
  - Forward delay, Turbo mode

---

## 🚨 Important Notes

> **Userbot Limitation** – Only **one userbot** can be added per user. The userbot, like any other bot, can run only **one forward at a time**. If you try to start another forward with the same userbot while it's busy, you'll get a warning.

> **Bot Concurrency** – You can run **multiple forwards simultaneously** as long as you use **different bots** (e.g., Bot1 and Bot2). The system prevents the same bot from running more than one forward.

> **Private Channels** – If your bot is **admin** in a private source channel, it will work without a userbot. Only when the bot cannot access the chat (e.g., not admin, not a member), the system will fall back to your userbot (if available).

> **Migration** – Existing users' bots are automatically migrated to the new multi-bot structure on first startup. No data loss.

---

## 🛠️ Variables

| Variable | Description |
|----------|-------------|
| `API_ID` | API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | API Hash from [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | Bot token from [@BotFather](https://t.me/BotFather) |
| `BOT_OWNER` | Telegram user ID of the owner (for owner commands) |
| `DATABASE_URI` | MongoDB URI (get from [MongoDB](https://mongodb.com)) |

---

## 🚀 Deployment

### Deploy to Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Codeflix-Bots/FileStore)

### Deploy to Koyeb
[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/Codeflix-Bots/FileStore&branch=master&name=master)

### Deploy to Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/deploy?template=https://github.com/Codeflix-Bots/FileStore)

### Deploy to Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Codeflix-Bots/FileStore)

### Deploy on VPS
```bash
git clone https://github.com/Codeflix-Bots/FileStore
cd FileStore
pip3 install -U -r requirements.txt
# Edit config.py with your variables
python3 main.py
