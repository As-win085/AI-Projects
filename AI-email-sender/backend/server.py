from xml.parsers.expat import model
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import smtplib, ssl, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/generate-email", methods=["POST"])
def generate_email():
    data = request.json
    prompt = data["prompt"]

    model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro if available
    response = model.generate_content([f"Write a professional email about: {prompt}"])


    return jsonify({"email": response.text})

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.json
    recipients = data["recipients"]
    subject = data.get("subject", "AI Generated Email")
    body = data["body"]

    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        for recipient in recipients:
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, recipient, message)

    return jsonify({"status": "Email Sent!"})

if __name__ == "__main__":
    app.run(debug=True)
