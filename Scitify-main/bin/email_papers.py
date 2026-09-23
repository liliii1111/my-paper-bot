import yagmail
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

# 清理可能存在的不可见字符（如换行符、空格）
sender_email = sender_email.strip()
sender_password = sender_password.replace(" ", "").replace("\n", "").replace("\r", "")
receiver_email = receiver_email.strip()

output_file = os.path.join(os.path.dirname(__file__), '../output/titles_and_urls.txt')
if not os.path.exists(output_file):
    print("No output file to send. No email sent.")
    sys.exit(0)

with open(output_file, 'r', encoding='utf-8') as f:
    content = f.read()

if not content.strip():
    print("Output file is empty. No email sent.")
    sys.exit(0)

try:
    # 使用 yagmail 发信，它会自动处理所有编码和服务器响应问题
    yag = yagmail.SMTP(user=sender_email, password=sender_password, host='smtp.gmail.com', port=465, smtp_ssl=True)
    yag.send(to=receiver_email, subject='PubMed 文献推送', contents=content)
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
