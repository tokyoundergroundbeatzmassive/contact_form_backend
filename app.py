import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def lambda_handler(event, context):
    data = json.loads(event['body'])
    
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not all([name, email, message]):
        return {
            'statusCode': 400,
            'body': json.dumps({"message": "Missing fields"})
        }

    sender_email = "xxx@example.xxx"
    receiver_email = "xxx@example.xxx"
    password = "your_app_pass"
    smtp_server = "smtp.zoho.xx"
    smtp_port = 465

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"New contact from {name}"

    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return {
            'statusCode': 200,
            'body': json.dumps({"message": "Email sent successfully"})
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({"message": "Failed to send email"})
        }