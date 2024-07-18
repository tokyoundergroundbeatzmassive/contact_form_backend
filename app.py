from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

app = Flask(__name__)
CORS(app)

with open('settings.json') as settings_file:
    settings = json.load(settings_file)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    if not data:
        return jsonify({"message": "No data provided"}), 400

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not all([name, email, message]):
        return jsonify({"message": "Missing fields"}), 400

    sender_email = settings['sender_email']
    receiver_email = settings['receiver_email']
    password = settings['password']
    smtp_server = settings['smtp_server']
    smtp_port = settings['smtp_port']

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
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to send email"}), 500

if __name__ == '__main__':
    app.run(debug=True)