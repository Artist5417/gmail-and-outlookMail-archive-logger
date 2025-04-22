import smtplib
import email
import json
import os
import mimetypes
from datetime import datetime
from email.message import EmailMessage

EMAIL_ACCOUNT = input("请输入您的 Outlook 邮箱地址: ").strip()
EMAIL_PASSWORD = input("请输入您的 App Password: ").strip()
JSON_FILE = input("请输入您的 JSON 文件名（默认 messages.json）: ").strip() or "messages.json"
dirs = input("请输入您存储附件的 Folder 名称（多个用逗号分隔，默认 files）: ").strip()
SEARCH_DIRS = [d.strip() for d in dirs.split(",")] if dirs else ["files"]

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

def load_messages(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def find_attachment(filepath):
    if os.path.isfile(filepath):
        return filepath
    filename = os.path.basename(filepath)
    for directory in SEARCH_DIRS:
        alt_path = os.path.join(directory, filename)
        if os.path.isfile(alt_path):
            return alt_path
    return None

def build_mime(message_data):
    msg = EmailMessage()
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = EMAIL_ACCOUNT
    msg["Subject"] = f"【{message_data['platform']}】归档消息"
    msg["Date"] = email.utils.format_datetime(datetime.strptime(message_data["timestamp"], "%Y-%m-%d %H:%M:%S"))
    body_text = (
        f"平台：{message_data['platform']}\n"
        f"发件人：{message_data['sender']}\n"
        f"收件人：{message_data['receiver']}\n"
        f"时间：{message_data['timestamp']}\n\n"
        f"内容：{message_data['content']}\n"
    )
    msg.set_content(body_text)
    for path in message_data.get("attachments", []):
        real_path = find_attachment(path)
        if real_path:
            with open(real_path, "rb") as f:
                data = f.read()
                ctype, _ = mimetypes.guess_type(real_path)
                maintype, subtype = ctype.split("/") if ctype else ("application", "octet-stream")
                filename = os.path.basename(real_path)
                msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)
        else:
            print(f"⚠ 附件未找到：{path}，已跳过。")
    return msg

def send_all():
    try:
        messages = load_messages(JSON_FILE)
    except FileNotFoundError:
        print(f"❌ 文件未找到：{JSON_FILE}")
        return

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        print("✅ 登录成功，开始发送消息...")
    except Exception as e:
        print("❌ 登录失败：", str(e))
        return

    for i, msg in enumerate(messages, 1):
        print(f"📨 正在发送第 {i} 条消息：{msg['platform']} {msg['timestamp']}")
        mime = build_mime(msg)
        try:
            server.send_message(mime)
            print("✅ 已发送")
        except Exception as e:
            print("❌ 发送失败：", str(e))

    server.quit()
    print("✅ 所有消息已处理，SMTP 会话已关闭")

if __name__ == "__main__":
    send_all()
