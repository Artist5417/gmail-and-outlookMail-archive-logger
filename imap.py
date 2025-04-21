import imaplib
import email
import json
import os
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import format_datetime

# 动态获取用户输入
EMAIL_ACCOUNT = input("请输入您的 Gmail 地址: ").strip()
EMAIL_PASSWORD = input("请输入您的 Gmail App Password: ").strip()
JSON_FILE = input("请输入您的JSON文件名（默认 messages.json）: ").strip() or "messages.json"

# 信息附件会存储在多个Folder中，以英文逗号分隔以便搜索
dirs = input("请输入您存储附件的Folder名称（多个Folder用逗号分隔，默认 files）: ").strip()
SEARCH_DIRS = [d.strip() for d in dirs.split(",")] if dirs else ["files"]

TARGET_FOLDER = '"[Gmail]/All Mail"'  # Gmail 归档目录

# 加载JSON中的数据
def load_messages(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

# 在多个目录里查找邮件
def find_attachment(filepath):
    if os.path.isfile(filepath):
        return filepath
    filename = os.path.basename(filepath)
    for directory in SEARCH_DIRS:
        alt_path = os.path.join(directory, filename)
        if os.path.isfile(alt_path):
            return alt_path
    return None

# 构造邮件
def build_mime(message_data):
    msg = EmailMessage()
    msg["From"] = message_data["sender"]
    msg["To"] = message_data["receiver"]
    msg["Subject"] = f"【{message_data['platform']}】归档消息"
    dt = datetime.strptime(message_data["timestamp"], "%Y-%m-%d %H:%M:%S")
    msg["Date"] = format_datetime(dt)

    body_text = (
        f"平台：{message_data['platform']}\n"
        f"发件人：{message_data['sender']}\n"
        f"收件人：{message_data['receiver']}\n"
        f"时间：{message_data['timestamp']}\n\n"
        f"内容：{message_data['content']}\n"
    )
    msg.set_content(body_text)

    attachments = message_data.get("attachments", [])
    if attachments:
        msg.make_mixed()
        for path in attachments:
            real_path = find_attachment(path)
            if real_path:
                with open(real_path, "rb") as f:
                    data = f.read()
                    maintype, subtype = "application", "octet-stream"
                    if real_path.lower().endswith((".jpg", ".jpeg")):
                        maintype, subtype = "image", "jpeg"
                    elif real_path.lower().endswith(".png"):
                        maintype, subtype = "image", "png"
                    elif real_path.lower().endswith(".pdf"):
                        maintype, subtype = "application", "pdf"
                    filename = os.path.basename(real_path)
                    msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)
            else:
                print(f"⚠ 附件未找到：{path}，已跳过。")
    return msg.as_bytes()

# 写入 Gmail All Mail(Archive)
def write_to_gmail_archive(mime_bytes):
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        imap.select(TARGET_FOLDER)
        now = datetime.now(timezone.utc)
        res = imap.append(TARGET_FOLDER, None, imaplib.Time2Internaldate(now), mime_bytes)
        imap.logout()
        print("✅ 写入成功：", res)
    except Exception as e:
        print(f"❌ 写入失败：{e}")

# 主程序入口
if __name__ == "__main__":
    try:
        messages = load_messages(JSON_FILE)
    except FileNotFoundError:
        print(f"❌ 文件未找到：{JSON_FILE}")
        exit(1)

    for i, msg in enumerate(messages, 1):
        print(f"\n📨 正在写入第 {i} 条消息：{msg['platform']} {msg['timestamp']}")
        mime_bytes = build_mime(msg)
        write_to_gmail_archive(mime_bytes)


