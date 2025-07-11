import os
import telebot
import openai
from flask import Flask
import threading
import sys

# ✅ Lấy token và API key từ biến môi trường
BOT_TOKEN = os.environ.get("7993764210:AAGnM45yo0rRwqHoRh7pN5W-C10NdJ-b8QI")
OPENAI_API_KEY = os.environ.get("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")

# ✅ Kiểm tra nếu thiếu thì dừng lại
if not BOT_TOKEN:
    print("❌ BOT_TOKEN chưa được cấu hình trong biến môi trường.")
    sys.exit()

if not OPENAI_API_KEY:
    print("❌ OPENAI_API_KEY chưa được cấu hình trong biến môi trường.")
    sys.exit()

# ✅ Khởi tạo bot và OpenAI
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
openai.api_key = OPENAI_API_KEY

# ✅ Lệnh /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "<b>🤖 Tôi là GPT DO TẤN KIỆT TẠO RA</b>", parse_mode="HTML")

# ✅ Lệnh /ask
@bot.message_handler(commands=['ask'])
def handle_ask(message):
    user_input = message.text.replace("/ask", "", 1).strip()
    if not user_input:
        bot.reply_to(message, "<b>❓ Hãy nhập nội dung sau lệnh /ask</b>", parse_mode="HTML")
        return
    loading = bot.reply_to(message, "🧠 Đang suy nghĩ...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        answer = response.choices[0].message.content.strip()
        formatted = f"<pre><b>{answer}</b></pre>"
        bot.edit_message_text(formatted, chat_id=message.chat.id, message_id=loading.message_id, parse_mode="HTML")
    except Exception as e:
        bot.edit_message_text("❌ Lỗi GPT. Kiểm tra lại API key hoặc nội dung!", chat_id=message.chat.id, message_id=loading.message_id)
        print(f"[GPT ERROR] {e}")

# ✅ Flask giữ bot sống trên Render
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "🤖 Bot GPT đang chạy!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

# ✅ Chạy Flask trong luồng riêng
threading.Thread(target=run_flask).start()

# ✅ Bắt đầu polling bot
print("🤖 Bot GPT đã khởi động!")
bot.infinity_polling()
