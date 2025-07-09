import logging
import os
import time
import subprocess
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
# Import thư viện chuẩn
import time

import io
from datetime import timedelta
import os
import tempfile
from gtts import gTTS
# Import thư viện bên thứ ba
import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
# Cấu hình logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Cài đặt bot
BOT_TOKEN = "7797658812:AAH_tyChkSFoZIfeCP-BB5naqRpprsqKUfw"
ADMIN_ID = 6043728545
blocked_users = []
allowed_users = []
cooldown_dict = {}

# Khởi tạo ứng dụng bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

async def spamvip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Kiểm tra nếu tin nhắn được gửi từ nhóm hợp lệ
    chat_id = update.message.chat_id
    if chat_id != ALLOWED_GROUP_ID:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Bot chỉ có thể hoạt động trong nhóm này!",
        )
        return
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Không xác định"
    message_id = update.message.message_id
    current_time = time.time()

    # Kiểm tra quyền truy cập
    if user_id not in allowed_users:
        await update.message.reply_text(
            "<blockquote><b>Sử dụng /napvip để nạp và sử dụng spamvip</b></blockquote>",
            parse_mode="HTML",
        )
        return

    # Kiểm tra cooldown (30 giây)
    if username in cooldown_dict and current_time - cooldown_dict[username].get("free", 0) < 30:
        remaining_time = int(30 - (current_time - cooldown_dict[username].get("free", 0)))
        await update.message.reply_text(
            f"<blockquote>@{username} Vui lòng đợi {remaining_time} giây trước khi sử dụng lại lệnh /spamvip.</blockquote>",
            parse_mode="HTML",
        )
        return

    # Cập nhật thời gian cooldown
    cooldown_dict[username] = {"free": current_time}

    # Phân tích cú pháp lệnh
    params = context.args
    if len(params) < 2:
        await update.message.reply_text("Thiếu thông tin (VD: /spamvip 0987654321 100).")
        return

    phone_number = params[0]
    try:
        num_spams = int(params[1])
        if num_spams < 20 or num_spams > 200:
            await update.message.reply_text("Số lần spam phải lớn hơn 20 và nhỏ hơn 200.")
            return
    except ValueError:
        await update.message.reply_text("Số lần spam không hợp lệ. Vui lòng nhập số nguyên lớn hơn 20.")
        return

    # Kiểm tra số điện thoại admin
    if phone_number in ["03939456755"]:
        await update.message.reply_text("Bot của anh nên anh sẽ không bị spam =))")
        return

    # Thông tin spam
    name_bot = "@KLTOOLBOT"
    admin = "@ngotk999"
    today = datetime.now().strftime("%Y-%m-%d")
    video_url = "https://files.catbox.moe/08c1q8.mp4"

    # Nội dung gửi đi
    message_text = f'''
<b>                          🚀   BOT BY 
  TẤN KIỆT  🚀</b>
<blockquote><b>┌──────────⭓
│»👾{name_bot}
│»👤USER: @{username}                      
│»SPAM: 🚀SUCCESS🚀
│»GÓI🔰: ⭐VIP⭐
│»📞PHONE: {phone_number}
│»✈ADMIN: {admin}
│»⚔️INTERACTIONS: {num_spams}
│»📅TODAY : {today}
└───────────────[✓]
</b></blockquote>
'''

    # Gửi video kèm nội dung
    try:
        await update.message.reply_video(
            video=video_url,
            caption=message_text,
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Lỗi khi gửi video: {e}")
        await update.message.reply_text(
            "<blockquote><b>Không thể gửi video. Vui lòng thử lại sau.</b></blockquote>",
            parse_mode="HTML"
        )
        return

    # Tiến hành spam bằng subprocess
    file_path = os.path.join(os.getcwd(), "sms.py")
    try:
        process = subprocess.Popen(["python", file_path, phone_number, str(num_spams)])
        logging.info(f"Đã khởi chạy spam trên {phone_number} với {num_spams} lần.")
    except Exception as e:
        logging.error(f"Lỗi khi khởi chạy quá trình spam: {e}")

# Thêm handler cho lệnh /spamvip
app.add_handler(CommandHandler("spamvip", spamvip_command))

# Lệnh /addvip
async def addvip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text(
            "<blockquote><b>Tuổi gì đòi add</b></blockquote>",
            parse_mode="HTML"
        )
        return
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "<blockquote><b>ID đâu @ngotk999</b></blockquote>",
            parse_mode="HTML"
        )
        return
    
    user_id = int(context.args[0])
    
    # Kiểm tra nếu người dùng đã có trong danh sách allowed_users
    if user_id in allowed_users:
        await update.message.reply_text(
            f"<blockquote><b>id này add từ trước rồi {user_id}</b></blockquote>",
            parse_mode="HTML"
        )
        return
    
    # Thêm người dùng vào danh sách allowed_users
    allowed_users.append(user_id)
    await update.message.reply_text(
        f"<blockquote><b>Người dùng {user_id} đã được cấp quyền sử dụng /spamvip🌠</b></blockquote>",
        parse_mode="HTML"
    )

# Thêm handler cho lệnh /addvip
app.add_handler(CommandHandler("add", addvip_command))

# Xóa hàm bot tắt và các phần kiểm tra trạng thái bot

import locale
from datetime import datetime

from datetime import datetime

def format_date_vietnamese(date):
    weekdays = ["Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Năm", "Thứ sáu", "Thứ bảy", "chủ nhật"]
    months = ["tháng 1", "tháng 2", "tháng 3", "tháng 4", "tháng 5", "tháng 6", 
              "tháng 7", "tháng 8", "tháng 9", "tháng 10", "tháng 11", "tháng 12"]
    weekday = weekdays[date.weekday()]
    month = months[date.month - 1]
    return f"{weekday}, {date.day} {month} năm {date.year}"

today = format_date_vietnamese(datetime.now())
print(today)  # In kết quả ngày hiện tại

async def spam_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Kiểm tra nếu tin nhắn được gửi từ nhóm hợp lệ
    chat_id = update.message.chat_id
    if chat_id != ALLOWED_GROUP_ID:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Bot chỉ có thể hoạt động trong nhóm này https://t.me/Spamsmstracuuttvip",
        )
        return
    
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Không xác định"
    current_time = time.time()

    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "<blockquote><b>VUI LÒNG NHẬP SỐ ĐIỆN THOẠI VÀ SỐ LƯỢNG TIN NHẮN</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    phone_number = args[0]
    if not phone_number.isnumeric():
        await update.message.reply_text(
            "<blockquote><b>SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ!</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    try:
        repeat_count = int(args[1])
    except ValueError:
        await update.message.reply_text(
            "<blockquote><b>SỐ LƯỢNG TIN NHẮN PHẢI LÀ MỘT SỐ NGUYÊN</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    if repeat_count <= 0 or repeat_count > 30:
        await update.message.reply_text(
            "<blockquote><b>SỐ LƯỢNG TIN NHẮN PHẢI TỪ 1 ĐẾN 30.</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    # Danh sách số điện thoại bị cấm
    banned_numbers = ['113', '911', '114', '115', '+843929456755', '03994526755', '09285721953', '+849285721953']
    if phone_number in banned_numbers:
        await update.message.reply_text(
            "<blockquote><b>Yêu admin à mà spam</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    # Gửi video kèm theo nội dung
    file_path = os.path.join(os.getcwd(), "sms.py")
    try:
        process = subprocess.Popen(["python", file_path, phone_number, str(repeat_count)])
    except Exception as e:
        logging.error(f"Error starting spam process: {e}")
        await update.message.reply_text(
            "<blockquote><b>Có lỗi xảy ra khi gửi tin nhắn. Vui lòng thử lại sau.</b></blockquote>", 
            parse_mode='HTML'
        )
        return

    # Ghi lại thời gian để quản lý cooldown
    cooldown_dict[username] = {'free': current_time}

    # Lấy ngày hôm nay với định dạng tiếng Việt
    today = datetime.now().strftime("%A, %d tháng %m năm %Y")  # Thứ Ngày tháng năm

    # Đường dẫn video và nội dung gửi đi
    video_url = "https://files.catbox.moe/08c1q8.mp4"
    message_text = f'''
<b>                          🚀   BOT BY 
  TẤN KIỆT  🚀</b>
<blockquote><b>┌──────────⭓
│»👾KLTOOLBOT
│»👤USER: @{username}                      
│»SPAM: 🚀SUCCESS🚀
│»GÓI🔰: ⭐FREE⭐
│»📞PHONE: {phone_number}
│»✈ADMIN: @ngotk999
│»⚔️INTERACTIONS: {repeat_count}
│»📅TODAY : {today}
└───────────────[✓]
</b></blockquote>
'''
    try:
        await update.message.reply_video(
            video_url,
            caption=message_text,
            parse_mode='HTML'
        )
    except Exception as e:
        logging.error(f"Error sending video: {e}")
        await update.message.reply_text(
            "<blockquote><b>Không thể gửi video. Vui lòng thử lại sau.</b></blockquote>", 
            parse_mode='HTML'
        )
                
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        # Kiểm tra nếu tin nhắn được gửi từ nhóm hợp lệ
        chat_id = update.message.chat_id
        if chat_id != ALLOWED_GROUP_ID:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Bot chỉ có thể hoạt động trong nhóm này https://t.me/Spamsmstracuuttvip",
            )
            return

        await update.message.reply_text("Vui lòng nhập tên thành phố sau lệnh /thoitiet.")
        return
    
    city = " ".join(context.args)
    weather_info = get_weather(city)
    await update.message.reply_text(weather_info, parse_mode="Markdown")

# Hàm lấy thông tin thời tiết
def get_weather(city):
    api_key = "93186fbb60d2143b81bf6ff558809c58"  # API key thời tiết
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric&lang=vi"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temp = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"]
        
        temp_emoji = "❄️" if temp < 15 else "🌡️" if temp < 30 else "☀️"
        temp_bar = "🌡️" * (int(temp) // 5)
        
        return (
            f"> 🌍 Thời tiết tại {city}:\n"
            f"{temp_emoji} Nhiệt độ: {temp}°C {temp_bar}\n"
            f"💨 Áp suất: {pressure} hPa\n"
            f"💧 Độ ẩm: {humidity}%\n"
            f"🌦️ Mô tả: {description.capitalize()}"
        )
    else:
        return "❌ Không tìm thấy thông tin cho thành phố này."

app.add_handler(CommandHandler("thoitiet", weather))
        
app.add_handler(CommandHandler("spam", spam_command))
        
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Cấu hình logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ID của nhóm mà bot sẽ hoạt động (Bạn cần lấy ID nhóm của bạn và thay thế vào đây)
ALLOWED_GROUP_ID = -1002403107765  # Thay thế bằng ID nhóm của bạn

# Thời gian bắt đầu bot
start_time = datetime.now()

start_time = time.time()
last_command_time = {}
def get_elapsed_time():
    elapsed_time = time.time() - start_time
    return str(timedelta(seconds=int(elapsed_time)))
async def send_time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    current_time = time.time()
    if user_id in last_command_time:
        elapsed_since_last = current_time - last_command_time[user_id]
        if elapsed_since_last < 5:
            wait_time = 5 - int(elapsed_since_last)
            await update.message.reply_text(f"Vui lòng đợi {wait_time} giây trước khi nhập lại lệnh.")
            return
    last_command_time[user_id] = current_time
    elapsed_time = get_elapsed_time()

    image_url = 'https://files.catbox.moe/tfkh8a.jpg'
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))

    try:
        font = ImageFont.truetype("arial.ttf", 90)
    except IOError:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(img)
    text = f"{elapsed_time}"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    image_width, image_height = img.size
    x_position = (image_width - text_width) // 2 - 85
    y_position = image_height - text_height - 120 
    glow_radius = 8  
    glow_color = (255, 69, 0)  # Màu lửa (rực lửa)
    for offset in range(-glow_radius, glow_radius + 1, 3):
        draw.text((x_position + offset, y_position + offset), text, font=font, fill=glow_color + (int(255 - abs(offset) * 10),))
    draw.text((x_position, y_position), text, font=font, fill="yellow")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    caption = f"\nBOT ĐÃ HOẠT ĐỘNG ĐƯỢC:"
    await update.message.reply_photo(img_byte_arr, caption=caption)
app.add_handler(CommandHandler("time", send_time_command))
  
# Lệnh /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id != ALLOWED_GROUP_ID:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Bot chỉ có thể hoạt động trong nhóm này!",
        )
        return
    
    help_text = """
<blockquote expandable>
<b>Hướng dẫn sử dụng bot SPAM:</b>
<b>/spam</b> - SPAM
<b>/spamvip</b> - spam VIP
<b>/time</b> - TIMEBOT
<b>/help</b> - lệnh
<b>/ask</b> - Chat AI
<b>/voice</b> - text - voice
<b>/qr</b> - tạo mã qr
<b>/info</b> - thông tin acc
<b>/thoitiet</b> - thoitiet
</blockquote>
"""
    await update.message.reply_text(help_text, parse_mode='HTML')

app.add_handler(CommandHandler("help", help_command))

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Hàm lấy thông tin thời tiết hiện tại
def get_weather(city):
    api_key = "93186fbb60d2143b81bf6ff558809c58"  # API key thời tiết
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric&lang=vi"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]
        clouds = data["clouds"]
        rain = data.get("rain", {}).get("1h", 0)

        city_name = data["name"]
        country = data["sys"]["country"]
        temp = main["temp"]
        feels_like = main["feels_like"]
        temp_max = main["temp_max"]
        temp_min = main["temp_min"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        description = weather["description"]
        wind_speed = wind["speed"]
        wind_deg = wind.get("deg", "N/A")
        cloudiness = clouds["all"]

        # Tạo kết quả dạng chuỗi
        weather_report = (
            f"🔆Thông Tin Thời Tiết cho @{city} ở {city_name}\n"
            f"│🌍 Thành phố: {city_name}\n"
            f"│🔗 Link bản đồ: [Xem bản đồ](https://www.google.com/maps/search/?api=1&query={city_name})\n"
            f"│☁️ Thời tiết: {description.capitalize()}\n"
            f"│🌡 Nhiệt độ hiện tại: {temp}°C\n"
            f"│🌡️ Cảm giác như: {feels_like}°C\n"
            f"│🌡️ Nhiệt độ tối đa: {temp_max}°C\n"
            f"│🌡️ Nhiệt độ tối thiểu: {temp_min}°C\n"
            f"│🍃 Áp suất: {pressure} hPa\n"
            f"│🫧 Độ ẩm: {humidity}%\n"
            f"│☁️ Mức độ mây: {cloudiness}%\n"
            f"│🌬️ Tốc độ gió: {wind_speed} m/s\n"
            f"│🌐 Quốc gia: {country}\n"
            f"│🌬 Hướng gió: {wind_deg}°\n"
            f"│☀️ Chỉ số UV: Không có thông tin\n"
            f"│🌧 Lượng mưa: {rain} mm\n"
            f"│🌧 Phần trăm lượng mưa: Không có thông tin"
        )
        return weather_report
    else:
        return "❌ Không tìm thấy thông tin cho thành phố này."

# Hàm xử lý lệnh "/thoitiet"
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Vui lòng nhập tên thành phố sau lệnh /thoitiet.")
        return
    
    city = " ".join(context.args)
    weather_info = get_weather(city)
    await update.message.reply_text(weather_info, parse_mode="Markdown")

# Thêm handler cho lệnh /thoitiet
app.add_handler(CommandHandler("thoitiet", weather))

async def text_to_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text[len('/voice '):].strip()


    if not text:
        await message.reply("🤖 KLT-BOT\nUsage: /voice <Text>")
        return

    # Tạo tệp tạm thời để lưu file .mp3
    temp_file_path = tempfile.mktemp(suffix='klt.mp3')

    try:

        tts = gTTS(text, lang='vi')
        tts.save(temp_file_path)

  
        with open(temp_file_path, 'rb') as audio_file:
            username = message.from_user.username or "Anonymous"
            cap = f"<blockquote>Nội dung : <code>{text}</code>\nĐược yêu cầu bởi: @{username}</blockquote>"
            await message.reply_voice(voice=audio_file, caption=cap, parse_mode="HTML")

    except Exception as e:
        logger.error(f"Error: {e}")
        await message.reply("🤖 KLT-BOT\nĐã xảy ra lỗi khi xử lý yêu cầu của bạn.")
    
    finally:
    
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

app.add_handler(CommandHandler("voice", text_to_voice))

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)

    # Lấy các key đã lưu từ file
    keys = load_keys()

    # Kiểm tra xem người dùng có key hợp lệ chưa
    if user_id not in keys:
        await update.message.reply_text("❌ Bạn chưa nhập key hợp lệ. Vui lòng sử dụng /getkey và nhập key của bạn.")
        return

    # Tách từ khóa nhập vào lệnh
    input_text = update.message.text.split(maxsplit=1)
    
    if len(input_text) > 1:
        input_text = input_text[1]  # Lấy phần từ khóa sau /qr
        
        try:
            # Tạo QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(input_text)
            qr.make(fit=True)
            
            img = qr.make_image(fill='black', back_color='white')
            bio = BytesIO()
            bio.name = 'qr.png'
            img.save(bio, 'PNG')
            bio.seek(0)

            # Tạo thông tin chi tiết về QR
            caption = (
                "<pre>     🚀 THÔNG TIN QR 🚀\n"
                "┌──────────⭓QR INFO⭓─────────\n"
                f"│» 🆔: {user_id}\n"
                f"│» 🔠Dữ liệu QR: {input_text}\n"
                f"│» 📏Chiều dài dữ liệu: {len(input_text)} ký tự\n"
                f"│» 📊Kiểu mã QR: {qr.get_matrix()}\n"
                "└───────────────[✓]─────────────</pre>"
            )

            # Gửi ảnh QR và thông tin chi tiết cho người dùng
            await update.message.reply_photo(photo=bio, caption=caption, parse_mode="HTML")
        except Exception as e:
            await update.message.reply_text(f"❌ Đã có lỗi xảy ra khi tạo QR: {str(e)}")
    else:
        await update.message.reply_text("🤖 Pixel-BOT\n🤖 Usage: /qr <Chữ Cần Tạo QR>")

app.add_handler(CommandHandler("qr", generate_qr))

async def handle_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user

    # Hiển thị biểu tượng đợi
    waiting_message = await update.message.reply_text("🔎 Đang xử lý...")

    try:
        # Lấy thông tin người dùng
        user_photos = await context.bot.get_user_profile_photos(user.id)
        chat_info = await context.bot.get_chat(user.id)
        chat_member = await context.bot.get_chat_member(update.message.chat.id, user.id)

        bio = chat_info.bio or "Không có bio"
        user_first_name = user.first_name
        user_last_name = user.last_name or ""
        user_username = f"@{user.username}" if user.username else "Không có username"
        user_language = user.language_code or "Không xác định"
        
        # Định nghĩa trạng thái người dùng
        status_dict = {
            "creator": "Admin chính",
            "administrator": "Admin",
            "member": "Thành viên",
            "restricted": "Bị hạn chế",
            "left": "Rời nhóm",
            "kicked": "Bị đuổi khỏi nhóm"
        }
        status = status_dict.get(chat_member.status, "Không xác định")
        
        # Soạn tin nhắn gửi đi
        caption = (
            "<pre>     🚀 THÔNG TIN 🚀\n"
            "┌──────────⭓INFO⭓─────────\n"
            f"│» 🆔: {user.id}\n"
            f"│» 👤Tên: {user_first_name} {user_last_name}\n"
            f"│» 👉Username: {user_username}\n"
            f"│» 🔰Ngôn ngữ: {user_language}\n"
            f"│» 🏴Trạng thái: {status}\n"
            f"│» ✍️Bio: {bio}\n"
            f"│» 🤳Avatar: {'Đã có avatar' if user_photos.total_count > 0 else 'Không có avatar'}\n"
            "└───────────────[✓]─────────────</pre>"
        )

        # Gửi ảnh hoặc tin nhắn văn bản
        if user_photos.total_count > 0:
            await context.bot.send_photo(
                chat_id=update.message.chat.id,
                photo=user_photos.photos[0][-1].file_id,
                caption=caption,
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(caption, parse_mode="HTML")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Đã xảy ra lỗi khi lấy thông tin: {str(e)}")
    
    # Xóa tin nhắn đợi
    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=waiting_message.message_id)
    
app.add_handler(CommandHandler("info", handle_check))    

if __name__ == "__main__":
    app.run_polling()
