# gmail-archive-logger

**Gmail Archive Logger** is a lightweight Python tool that helps you archive short messages — including text content and attachments such as images or PDFs — into Gmail’s **All Mail** folder using the IMAP protocol and MIME formatting. It is designed for customizable user input, fallback file searching, and clean automation.

---

## Why This Project

We all send and receive countless short messages every day — from casual conversations to memorable moments. The goal of this tool is to **preserve those fragments of life**, so that one day, you can look back and rediscover what you once said, felt, or planned — all archived safely in your Gmail.

Choosing the **All Mail** folder ensures that these archived messages **do not clutter your Inbox**, keeping your main interface clean while your memories are quietly stored in the background.

> ⚠️ Note: This project **does not handle scraping or exporting messages from platforms like WhatsApp, SMS, or Telegram**. It only reads messages already structured in a specific JSON format. Users are responsible for preparing or exporting their own message data.

---

## Features

- Archive any number of text messages to Gmail with correct timestamps
- Preserve attachments (PDFs, images)
- Fallback search: find attachment files even when paths are inaccurate
- Manual input of credentials — no hardcoding
- Clean output and user-friendly command line interface
- Non-intrusive: uses `[Gmail]/All Mail`, keeps Inbox tidy

---

## Usage

```bash
python imap.py
```

The script will prompt for:
- Your Gmail address  
- Gmail App Password  
- JSON file containing messages  
- One or more folders where attachments may be located (e.g. `files,Random`)

---
## How To Get Gmail App Passwords

Due to Gmail security policies, **regular passwords will not work**. You must:
1. Enable 2-Step Verification in your Google account  
2. Create an App Password for "Mail"  
3. Use that password when prompted

More info: [https://myaccount.google.com/security](https://myaccount.google.com/security)

---

## Installation

```bash
git clone https://github.com/Artist5417/gmail-archive-logger.git
cd gmail-archive-logger
pip install -r requirements.txt  # (if applicable)
```
> Python 3.7+ recommended

---

## JSON Format Example

```json
[
  {
    "platform": "WhatsApp",
    "sender": "user@example.com",
    "receiver": "me@example.com",
    "timestamp": "2025-04-20 09:00:00",
    "content": "This is a test message with an image.",
    "attachments": ["files/photo1.jpg"]
  },
  {
    "platform": "SMS",
    "sender": "bank@example.com",
    "receiver": "me@example.com",
    "timestamp": "2025-04-20 10:00:00",
    "content": "Your verification code is 123456."
  }
]
```

> ⚠️ Currently supported attachment formats: `.jpg`, `.jpeg`, `.png`, `.pdf`  
> You can extend support for other types by editing the MIME detection logic in `imap.py`.

---

## 📬 Output

All archived messages will appear in your Gmail **All Mail** folder with:
- Correct timestamp
- Preserved content and sender/receiver
- Attachments (if available)

---

## 🔧 Customization

- Feel free to modify the `messages.json` file to suit your message schema.
- You can add more attachment types by modifying the `build_mime_message()` function.

---


