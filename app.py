import openai
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Mã xác minh webhook (Thay đổi giá trị này khi điền vào Facebook Developer)
VERIFY_TOKEN = "sangnguyen"

# Thay API Key của bạn ở đây
OPENAI_API_KEY = "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"

def chat_with_ai(user_message):
    """Gửi tin nhắn đến OpenAI và nhận phản hồi"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Bạn là một chatbot AI thông minh giúp khách hàng mua sắm."},
            {"role": "user", "content": user_message}
        ]
    )
    return response["choices"][0]["message"]["content"]

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """Xác minh Webhook với Facebook"""
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if token == VERIFY_TOKEN:
        return challenge
    return "Xác minh thất bại", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    """Nhận tin nhắn từ Messenger & TikTok"""
    data = request.json
    if "message" in data:
        user_message = data["message"]["text"]
        ai_response = chat_with_ai(user_message)
        return jsonify({"reply": ai_response})
    
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
