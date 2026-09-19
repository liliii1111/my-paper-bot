import smtplib
from email.mime.text import MIMEText
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
receiver_email = args.receiver_email

with open(config_path, 'r', encoding='utf-8') as f:
    for line in f:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            if key.strip() == 'sender_email': sender_email = value.strip()
            if key.strip() == 'sender_password': sender_password = value.strip()
            if key.strip() == 'receiver_email': receiver_email = value.strip()

output_file = os.path.join(os.path.dirname(__file__), '../output/titles_and_urls.txt')
if not os.path.exists(output_file):
    print("No output file to send. No email sent.")
    sys.exit(0)

with open(output_file, 'r', encoding='utf-8') as f:
    content = f.read()

if not content.strip():
    print("Output file is empty. No email sent.")
    sys.exit(0)

smtp_server = 'smtp.163.com'
smtp_port = 465

msg = MIMEText(content, 'plain', 'utf-8')
msg['Subject'] = 'PubMed 文献推送'
msg['From'] = sender_email
msg['To'] = receiver_email

try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, [receiver_email], msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
