from telethon import TelegramClient, events
import smtplib
from email.mime.text import MIMEText
import config

# 创建 Telegram 客户端
client = TelegramClient('session', config.API_ID, config.API_HASH)

# 邮件发送函数
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config.EMAIL_FROM
    msg['To'] = config.EMAIL_TO

    server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    server.starttls()
    server.login(config.EMAIL_FROM, config.EMAIL_PASSWORD)
    server.sendmail(config.EMAIL_FROM, [config.EMAIL_TO], msg.as_string())
    server.quit()

# ✅ 监听主频道：轻舟已过万重山（频道ID）
@client.on(events.NewMessage(chats=config.TELEGRAM_GROUP))
async def main_channel_handler(event):
    text = event.message.message
    print(f"[主频道] 新消息：{text}")
    send_email("Telegram群新消息 - 轻舟已过万重山", text)

# ✅ 监听测试频道：请在 config.py 中添加 TEST_GROUP_ID
@client.on(events.NewMessage(chats=config.TEST_GROUP_ID))
async def test_channel_handler(event):
    text = event.message.message
    print(f"[测试频道] 新消息：{text}")
    send_email("Telegram测试频道新消息", text)

# 启动监听
client.start(phone=config.PHONE_NUMBER)
client.run_until_disconnected()
