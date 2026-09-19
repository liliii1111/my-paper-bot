import smtplib
from email.mime.text import MIMEText
from email.header import Header
import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--service', type=str)
parser.add_argument('--receiver_email', type=str)
args = parser.parse_args()

config_path = os.path.join(os.path.dirname(__file__), '../config/paper_update_config.txt')
sender_email = ''
sender_password = ''
receiver_email = str(args.receiver_email)

with open(config_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if key == 'sender_email': sender_email = value
            if key == 'sender_password': sender_password = value
            if key == 'receiver_email': receiver_email = value

output_file = os.path.join(os.path.dirname(__file__), '../output/titles_and_urls.txt')
if not os.path.exists(output_file):
    print("No output file to send. No email sent.")
    sys.exit(0)

with open(output_file, 'r', encoding='utf-8') as f:
    content = f.read()

if not content.strip():
    print("Output file is empty. No email sent.")
    sys.exit(0)

# 强制转换为干净的字符串
sender_email = str(sender_email).strip()
sender_password = str(sender_password).strip()
receiver_email = str(receiver_email).strip()

smtp_server = 'smtp.163.com'
smtp_port = 465

msg = MIMEText(content, 'plain', 'utf-8')
msg['Subject'] = Header('PubMed 文献推送', 'utf-8')
msg['From'] = sender_email
msg['To'] = receiver_email

try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.encoding = 'utf-8'  # 关键修复！让 smtplib 用 UTF-8 解析响应，避免 bytes 拼接错误
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, [receiver_email], msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
