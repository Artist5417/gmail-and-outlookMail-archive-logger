# gmail-and-outlook-archive-logger

**Gmail & Outlook Archive Logger** is a lightweight Python tool that helps you archive short messages — including text content and attachments such as images or PDFs — into Gmail’s **All Mail** folder or Outlook’s **Inbox**, using the IMAP or SMTP protocol with MIME formatting. It is designed for customizable user input, fallback file searching, and clean automation.

---

## 📌 Why This Project

We all send and receive countless short messages every day — from casual conversations to meaningful details. The goal of this tool is to **preserve those fragments of life**, so that one day, you can look back and rediscover what you once said, felt, or planned — all safely archived in your email.

Choosing Gmail’s **All Mail** folder ensures that these messages **do not clutter your Inbox**, keeping your main interface clean while your memories are quietly stored in the background. When using Outlook, messages are written into the **Inbox**, as direct access to Archive is restricted via SMTP.

> ⚠️ Note: This project does **not handle scraping or exporting** messages from platforms like WhatsApp, SMS, or Telegram. It only reads from pre-formatted JSON files. Users must prepare their own message data.

---

## ✅ Features

- Archive any number of short messages to Gmail or Outlook
- Preserves full metadata: timestamp, sender, receiver, content
- Supports a wide range of file types as attachments (e.g. `.pdf`, `.jpg`, `.txt`, `.mp3`, `.avi`, etc.)
- Smart fallback search for attachments with correct file name and format, even if the path is unclear
- Clean command-line interface with no hardcoded values
- Dual-protocol support:
  - **IMAP** for Gmail (writes to `[Gmail]/All Mail`)
  - **SMTP** for Outlook (writes to `Inbox`)

---

## 🚀 Usage

The script will prompt for:
- **Your email address**
- **App password** (Gmail or Outlook)
- **JSON file** containing the messages
- **Attachment folder(s)**: one or more directories where attachments may be located  
  (e.g. `files`, `docs`, or `files,images`)

After reading the JSON, each message is parsed, converted into MIME format, and sent to the selected email platform. Attachments are matched by filename across fallback directories. If not found, they are skipped with a warning.

---

## 📩 Gmail Setup

To use this script with Gmail:

1. Enable 2-Step Verification in your Google Account  
2. Create an App Password for "Mail"  
3. Use that App Password when prompted

> Regular Gmail password will **not** work due to security policies.

📎 App Passwords: [https://myaccount.google.com/security](https://myaccount.google.com/security)

---

## 📬 Outlook Notes

To use this script with Outlook (SMTP method):

- The Outlook account must have **SMTP enabled**
- 2FA (Two-Step Verification) is **recommended**
- You must create an **App Password** under Security settings

If you're part of an organization, make sure the admin **allows legacy protocols like SMTP** or permits App Passwords.

---

## 🚀 Installation

```bash
git clone https://github.com/Artist5417/gmail-and-outlook-archive-logger.git
cd gmail-archive-logger
pip install -r requirements.txt  # (if applicable)

---

## 📄 JSON Format Example

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

---

## 📥 Output

- Gmail users: messages appear in **All Mail** folder  
- Outlook users: messages go to **Inbox**
- Each message contains:
  - Proper timestamp
  - Sender/receiver info
  - Full message content
  - Attachments (if available)

---

## 🔧 Customization

- You can edit `messages.json` to suit your own data export format.
- You can adjust the Python script to support more MIME types or to change folders.
- Currently supports `.jpg`, `.png`, `.pdf`, `.docx`, `.txt`, `.mp3`, `.avi`, and other common types.



