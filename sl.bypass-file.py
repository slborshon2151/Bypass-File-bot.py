import telebot
from telebot import types
import os
import json
from datetime import datetime
from flask import Flask
from threading import Thread, Lock
import logging
from dotenv import load_dotenv

# Environment ভেরিয়েবল লোড করুন
load_dotenv()

# Logging সেটআপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask সার্ভার সেটআপ
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run, daemon=True)
    t.start()

# Configuration - Environment ভেরিয়েবল থেকে লোড করুন
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
CHANNELS = os.getenv('CHANNELS', '-1002779233092').split(',')
LINK = os.getenv('CHANNEL_LINK', 'https://t.me/xxxxx')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', '@admin')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))

# ডাটা ফাইল পাথ
USER_FILE = "users.txt"
USER_DATA_FILE = "user_details.txt"
LINKS_JSON = "file_links.json"

# গ্লোবাল ডাটা স্টোর
FILE_LINKS = {}
pending_data = {}
data_lock = Lock()  # থ্রেড সেফটির জন্য

# বট ইনিশিয়েলাইজ করুন
bot = telebot.TeleBot(API_TOKEN)

# ==================== HELPER FUNCTIONS ====================

def load_links():
    """লিঙ্ক ফাইল লোড করুন ডিফল্ট ভ্যালু সহ"""
    DEFAULT_LINKS = {
        "Ryze-BD🇧🇩.dark": "https://t.me/xxxxxxxxxxxxbd/366x",
        "Ryze-SG🇸🇬.dark": "https://t.me/xxxxxxxxxxxxbd/221x", 
        "Ryze-IN🇮🇳.dark": "https://t.me/xxxxxxxxxxxxbd/348x",
        "Stream-BD🇧🇩.dark": "https://t.me/xxxxxxxxxxxxbd/368x", 
        "Stream-SG🇸🇬.dark": "https://t.me/xxxxxxxxxxxxbd/223x",   
        "Stream-IN🇮🇳.dark": "https://t.me/xxxxxxxxxxxxbd/350x",
        "Social-BD🇧🇩.dark": "https://t.me/xxxxxxxxxxxxbd/367x", 
        "Social-SG🇸🇬.dark": "https://t.me/xxxxxxxxxxxxbd/222x", 
        "Social-IN🇮🇳.dark": "https://t.me/xxxxxxxxxxxxbd/349x",
        "Ott-BD🇧🇩.dark": "https://t.me/xxxxxxxxxxxxbd/364x",
        "Ott-SG🇸🇬.dark": "https://t.me/xxxxxxxxxxxxbd/219x",
        "Ott-IN🇮🇳.dark": "https://t.me/xxxxxxxxxxxxbd/346x",
        "Robi-BD🇧🇩.dark": "https://t.me/xxxxxxxxxxxxbd/365x",
        "Robi-SG🇸🇬.dark": "https://t.me/xxxxxxxxxxxxbd/220x",
        "Robi-IN🇮🇳.dark": "https://t.me/xxxxxxxxxxxxbd/347x",
        "Airtel-200-BD🇧🇩.dark": "https://t.me/xxxxxxxxxxxxbd/363x",
        "Airtel-200-SG🇸🇬.dark": "https://t.me/xxxxxxxxxxxxbd/218x",
        "Airtel-200-IN🇮🇳.dark": "https://t.me/xxxxxxxxxxxxbd/345x",
        "Airtel-279-BD🇧🇩.dark": "https://t.me/xxxxxxxxxxxxbd/336x",
        "Airtel-279-SG🇸🇬.dark": "https://t.me/xxxxxxxxxxxxbd/336x",
        "Airtel-279-IN🇮🇳.dark": "https://t.me/xxxxxxxxxxxxbd/336x",
        "All Pack-BD🇧🇩.nm": "https://t.me/xxxxxxxxxxxxbd/371x",
        "All Pack-SG🇸🇬.nm": "https://t.me/xxxxxxxxxxxxbd/232x",
        "All Pack-IN🇮🇳.nm": "https://t.me/xxxxxxxxxxxxbd/354x",
    }
    
    try:
        if os.path.exists(LINKS_JSON):
            with open(LINKS_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"লিঙ্ক লোড করতে এরর: {e}")
    
    return DEFAULT_LINKS

def save_links(links):
    """লিঙ্ক ফাইল সেভ করুন"""
    try:
        with open(LINKS_JSON, "w", encoding="utf-8") as f:
            json.dump(links, f, ensure_ascii=False, indent=4)
        logger.info("লিঙ্ক সফলভাবে সেভ হয়েছে")
    except Exception as e:
        logger.error(f"লিঙ্ক সেভ করতে এরর: {e}")

FILE_LINKS = load_links()

def ensure_files_exist():
    """প্রয়োজনীয় ফাইল তৈরি করুন"""
    for file in [USER_FILE, USER_DATA_FILE]:
        if not os.path.exists(file):
            with open(file, "w", encoding="utf-8") as f:
                pass

ensure_files_exist()

def save_user(user):
    """নতুন ইউজার সেভ করুন"""
    user_id = str(user.id)
    first_name = user.first_name if user.first_name else "User"
    username = f"@{user.username}" if user.username else "N/A"
    
    try:
        with data_lock:
            with open(USER_FILE, "r", encoding="utf-8") as f:
                users = f.read().splitlines()
            
            if user_id not in users:
                with open(USER_FILE, "a", encoding="utf-8") as f:
                    f.write(user_id + "\n")
                
                with open(USER_DATA_FILE, "a", encoding="utf-8") as f:
                    f.write(f"Name: {first_name} | User: {username} | ID: {user_id}\n")
                
                notify_admin_new_user(user, len(users) + 1)
    except Exception as e:
        logger.error(f"ইউজার সেভ করতে এরর: {e}")

def notify_admin_new_user(user, total_users):
    """নতুন ইউজারের বিজ্ঞপ্তি পাঠান"""
    try:
        now = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
        user_name = user.username if user.username else 'N/A'
        caption = (
            f"📊 **নতুন ইউজারের বিস্তারিত তথ্য**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👤 **নাম:** {user.first_name}\n"
            f"🆔 **আইডি:** `{user.id}`\n"
            f"🏷️ **ইউজারনেম:** @{user_name}\n"
            f"🌐 **ল্যাঙ্গুয়েজ:** {user.language_code}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📈 **বটের মোট ইউজার:** {total_users}\n"
            f"⏰ **সময়:** {now} (BD)"
        )
        
        photos = bot.get_user_profile_photos(user.id)
        if photos.total_count > 0:
            bot.send_photo(ADMIN_ID, photos.photos[0][-1].file_id, caption=caption, parse_mode="Markdown")
        else:
            bot.send_message(ADMIN_ID, caption, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"অ্যাডমিনকে নোটিফাই করতে এরর: {e}")

def check_join(user_id):
    """চ্যানেলে জয়েন চেক করুন"""
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status in ['left', 'kicked']:
                return False
        except Exception as e:
            logger.error(f"চ্যানেল চেক করতে এরর: {e}")
            return False
    return True

def main_menu():
    """মেইন মেনু কীবোর্ড"""
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("DARK TUNNEL 🔑", "NETMOD VPN 🔑", "SUPPORT ☎️", "অভিযোগ 📝")
    return markup

# ==================== COMMAND HANDLERS ====================

@bot.message_handler(commands=['start'])
def start(message):
    """স্টার্ট কমান্ড হ্যান্ডলার"""
    save_user(message.from_user)
    
    if check_join(message.from_user.id):
        bot.send_message(message.chat.id, "🎉 স্বাগতম! আপনার প্রয়োজনীয় অপশনটি বেছে নিন।", reply_markup=main_menu())
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 জয়েন করুন", url=LINK))
        markup.add(types.InlineKeyboardButton("✅ ভেরিফাই করুন", callback_data="verify_join"))
        bot.send_message(message.chat.id, "⚠️ আগে চ্যানেলে জয়েন করুন।", reply_markup=markup)

@bot.message_handler(commands=['update'])
def update_link_cmd(message):
    """লিঙ্ক আপড���ট কমান্ড (শুধু অ্যাডমিনের জন্য)"""
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ আপনি অ্যাডমিন নন।")
        return
    
    try:
        markup = types.InlineKeyboardMarkup(row_width=1)
        current_links = load_links()
        
        for file_name in list(current_links.keys())[:10]:  # প্রথম ১০টি দেখান
            markup.add(types.InlineKeyboardButton(f"Update: {file_name}", callback_data=f"up_req_{file_name}"))
        
        bot.send_message(message.chat.id, "⚙️ আপনি কোন ফাইলটির লিঙ্ক পরিবর্তন করতে চান?", reply_markup=markup)
    except Exception as e:
        logger.error(f"আপডেট কমান্ডে এরর: {e}")
        bot.send_message(message.chat.id, f"❌ এরর: {e}")

@bot.message_handler(commands=['User-List'])
def user_list_cmd(message):
    """ইউজার লিস্ট কমান্ড (শুধু অ্যাডমিনের জন্য)"""
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ আপনি অ্যাডমিন নন।")
        return
    
    try:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
                data = f.read()
            
            if data.strip():
                if len(data) > 4000:
                    with open(USER_DATA_FILE, "rb") as f:
                        bot.send_document(message.chat.id, f, caption="📜 সম্পূর্ণ ইউজার লিস্ট")
                else:
                    bot.send_message(message.chat.id, f"📜 **ইউজার লিস্ট:**\n\n{data}", parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, "এখনো কোনো ইউজার নেই।")
    except Exception as e:
        logger.error(f"ইউজার লিস্টে এরর: {e}")
        bot.send_message(message.chat.id, f"❌ এরর: {e}")

@bot.message_handler(commands=['Admin-News'])
def admin_news_cmd(message):
    """অ্যাডমিন নিউজ কমান্ড"""
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ আপনি অ্যাডমিন নন।")
        return
    
    msg = bot.send_message(message.chat.id, "📝 সবাইকে পাঠানোর জন্য আপনার নিউজ মেসেজটি লিখুন (Text/Photo/Video):")
    bot.register_next_step_handler(msg, process_broadcast_step)

def process_broadcast_step(message):
    """ব্রডকাস্ট স্টেপ প্রসেস করুন"""
    with data_lock:
        pending_data['news_msg'] = message
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ হ্যাঁ, পাঠান", callback_data="send_news"),
               types.InlineKeyboardButton("❌ বাতিল", callback_data="cancel_news"))
    bot.send_message(message.chat.id, "⚠️ আপনি কি নিশ্চিত যে এই মেসেজটি সকল ইউজারকে পাঠাতে চান?", reply_markup=markup)

@bot.message_handler(commands=['Private-Msg'])
def private_msg_cmd(message):
    """প্রাইভেট মেসেজ কমান্ড"""
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ আপনি অ্যাডমিন নন।")
        return
    
    msg = bot.send_message(message.chat.id, "🎯 আপনি যাকে মেসেজ পাঠাতে চান তার **Chat ID** দিন:")
    bot.register_next_step_handler(msg, process_private_msg_id)

def process_private_msg_id(message):
    """প্রাইভেট মেসেজ আইডি প্রসেস করুন"""
    target_id = message.text.strip()
    
    if not target_id.isdigit():
        bot.send_message(message.chat.id, "⚠️ ভুল আইডি! শুধু সংখ্যা ব্যবহার করুন।")
        return
    
    with data_lock:
        pending_data[message.from_user.id] = {'target_id': target_id}
    
    msg = bot.send_message(message.chat.id, f"📝 আইডি `{target_id}` এর জন্য আপনার মেসেজটি লিখুন:", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_private_msg_content)

def process_private_msg_content(message):
    """প্রাইভেট মেসেজ কন্টেন্ট প্রসেস করুন"""
    admin_id = message.from_user.id
    
    with data_lock:
        if admin_id not in pending_data:
            bot.send_message(message.chat.id, "❌ সেশন এক্সপায়ার হয়েছে। আবার চেষ্টা করুন।")
            return
        
        pending_data[admin_id]['content'] = message
        target_id = pending_data[admin_id]['target_id']
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ পাঠান", callback_data="confirm_private"),
               types.InlineKeyboardButton("❌ বাতিল", callback_data="cancel_private"))
    
    bot.send_message(message.chat.id, f"⚠️ আপনি কি নিশ্চিত যে এই মেসেজটি আইডি `{target_id}`-এ পাঠাবেন?", 
                     parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "SUPPORT ☎️")
def support_handler(message):
    """সাপোর্ট হ্যান্ডলার"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📨 কন্টাক্ট অ্যাডমিন", url=f"https://t.me/{ADMIN_USERNAME.replace('@','')}"))
    bot.send_message(message.chat.id, "যোগাযোগ করতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "অভিযোগ 📝")
def complaint_start(message):
    """অভিযোগ শুরু করুন"""
    msg = bot.send_message(message.chat.id, "✍️ আপনার অভিযোগটি বিস্তারিত লিখুন:")
    bot.register_next_step_handler(msg, process_complaint_step)

def process_complaint_step(message):
    """অভিযোগ প্রসেস করুন"""
    user_id = message.from_user.id
    
    with data_lock:
        pending_data[user_id] = message.text
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ হ্যাঁ, পাঠান", callback_data="send_comp"),
               types.InlineKeyboardButton("❌ বাতিল", callback_data="cancel_comp"))
    
    bot.send_message(message.chat.id, 
                     f"⚠️ আপনি কি নিশ্চিত যে এই অভিযোগটি অ্যাডমিনের কাছে পাঠাতে চান?\n\n{message.text}", 
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "DARK TUNNEL 🔑")
def dark_tunnel_menu(message, is_edit=False):
    """ডার্ক টানেল মেনু"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    opts = [
        ("Ryze.dark 🌐", "dt_Ryze"), 
        ("Stream.dark 🌐", "dt_Stream"), 
        ("Social.dark 🌐", "dt_Social"), 
        ("Ott.dark 🌐", "dt_Ott"), 
        ("Robi-219-Tk.dark 🌐", "dt_Robi"), 
        ("Airtel-200-Tk.dark 🌐", "dt_Airtel-200"), 
        ("Airtel-279-Tk.dark 🌐", "dt_Airtel-279")
    ]
    for text, data in opts:
        markup.add(types.InlineKeyboardButton(text, callback_data=data))
    
    if is_edit:
        bot.edit_message_text("📂 DARK TUNNEL ক্যাটাগরি সিলেক্ট করুন:", message.chat.id, message.message_id, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "📂 DARK TUNNEL ক্যাটাগরি সিলেক্ট করুন:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "NETMOD VPN 🔑")
def netmod_vpn_menu(message, is_edit=False):
    """নেটমড ভিপিএন মেনু"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("All Pack.nm 🌐", callback_data="nm_all_pack"),
               types.InlineKeyboardButton("All Pack.Info ♾️", callback_data="nm_info"))
    
    if is_edit:
        bot.edit_message_text("📂 NETMOD VPN ক্যাটাগরি সিলেক্ট করুন:", message.chat.id, message.message_id, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "📂 NETMOD VPN ক্যাটাগরি সিলেক্ট করুন:", reply_markup=markup)

# ==================== CALLBACK HANDLERS ====================

@bot.callback_query_handler(func=lambda call: True)
def callback_all(call):
    """সমস্ত কলব্যাক কোয়েরি হ্যান্ডলার"""
    user_id = call.from_user.id
    
    try:
        # প্রাইভেট মেসেজ কনফার্ম
        if call.data == "confirm_private":
            with data_lock:
                data = pending_data.get(user_id)
                if not data:
                    bot.edit_message_text("❌ সেশন এক্সপায়ার হয়েছে।", call.message.chat.id, call.message.message_id)
                    return
                
                target = data['target_id']
                content = data['content']
            
            try:
                bot.copy_message(target, content.chat.id, content.message_id)
                bot.edit_message_text(f"✅ মেসেজটি আইডি `{target}`-এ সফলভাবে পাঠানো হয়েছে।", 
                                     call.message.chat.id, call.message.message_id, parse_mode="Markdown")
            except Exception as e:
                bot.edit_message_text(f"❌ মেসেজ পাঠানো যায়নি: {str(e)}", 
                                     call.message.chat.id, call.message.message_id)
            
            with data_lock:
                if user_id in pending_data:
                    del pending_data[user_id]
        
        # প্রাইভেট মেসেজ বাতিল
        elif call.data == "cancel_private":
            with data_lock:
                if user_id in pending_data:
                    del pending_data[user_id]
            bot.edit_message_text("❌ প্রাইভেট মেসেজ বাতিল করা হয়েছে।", 
                                 call.message.chat.id, call.message.message_id)
        
        # অভিযোগ পাঠান
        elif call.data == "send_comp":
            with data_lock:
                complaint_text = pending_data.get(user_id)
                if complaint_text:
                    bot.send_message(ADMIN_ID, 
                                   f"📩 **নতুন অভিযোগ!**\n\nইউজার: {call.from_user.first_name}\n🆔 আইডি: `{user_id}`\n\n📝 অভিযোগ: {complaint_text}",
                                   parse_mode="Markdown")
                    bot.edit_message_text("✅ আপনার অভিযোগটি অ্যাডমিনের কাছে সফলভাবে পাঠানো হয়েছে।", 
                                         call.message.chat.id, call.message.message_id)
                    del pending_data[user_id]
        
        # অভিযোগ বাতিল
        elif call.data == "cancel_comp":
            with data_lock:
                if user_id in pending_data:
                    del pending_data[user_id]
            bot.edit_message_text("❌ অভিযোগ বাতিল করা হয়েছে।", 
                                 call.message.chat.id, call.message.message_id)
        
        # নিউজ পাঠান
        elif call.data == "send_news":
            with data_lock:
                original_msg = pending_data.get('news_msg')
            
            if original_msg and os.path.exists(USER_FILE):
                bot.edit_message_text("⏳ ব্রডকাস্ট শুরু হয়েছে...", 
                                     call.message.chat.id, call.message.message_id)
                
                try:
                    with open(USER_FILE, "r", encoding="utf-8") as f:
                        users = f.read().splitlines()
                    
                    count = 0
                    failed = 0
                    
                    for user_uid in users:
                        try:
                            bot.copy_message(user_uid, original_msg.chat.id, original_msg.message_id)
                            count += 1
                        except Exception as e:
                            logger.warning(f"ব্যবহারকারী {user_uid}-এ ফেইল: {e}")
                            failed += 1
                    
                    bot.send_message(call.message.chat.id, 
                                   f"✅ নিউজ সফলভাবে {count} জন ইউজারের কাছে পাঠানো হয়েছে।\n❌ ফেইল: {failed}")
                    
                    with data_lock:
                        if 'news_msg' in pending_data:
                            del pending_data['news_msg']
                except Exception as e:
                    logger.error(f"ব্রডকাস্টে এরর: {e}")
                    bot.send_message(call.message.chat.id, f"❌ এরর: {e}")
        
        # নিউজ বাতিল
        elif call.data == "cancel_news":
            with data_lock:
                if 'news_msg' in pending_data:
                    del pending_data['news_msg']
            bot.edit_message_text("❌ নিউজ ব্রডকাস্ট বাতিল করা হয়েছে।", 
                                 call.message.chat.id, call.message.message_id)
        
        # জয়েন ভেরিফাই করুন
        elif call.data == "verify_join":
            if check_join(user_id):
                try:
                    bot.delete_message(call.message.chat.id, call.message.message_id)
                except:
                    pass
                bot.send_message(call.message.chat.id, "✅ ভেরিফিকেশন সফল!", reply_markup=main_menu())
            else:
                bot.answer_callback_query(call.id, "❌ জয়েন করেননি!", show_alert=True)
        
        # ব্যাক বাটন
        elif call.data == "back_to_dark":
            dark_tunnel_menu(call.message, is_edit=True)
        
        elif call.data == "back_to_netmod":
            netmod_vpn_menu(call.message, is_edit=True)
        
        # লিঙ্ক আপডেট রিকোয়েস্ট
        elif call.data.startswith('up_req_'):
            file_to_update = call.data.replace("up_req_", "")
            msg = bot.send_message(call.message.chat.id, f"🔗 `{file_to_update}` এর জন্য নতুন লিঙ্কটি পাঠান:", 
                                  parse_mode="Markdown")
            bot.register_next_step_handler(msg, process_update_link, file_to_update)
        
        # ডার্ক টানেল ক্যাটাগরি
        elif call.data.startswith('dt_'):
            category = call.data.replace("dt_", "")
            markup = types.InlineKeyboardMarkup(row_width=1)
            
            for country in ["BD🇧🇩", "SG🇸🇬", "IN🇮🇳"]:
                file_name = f"{category}-{country}.dark"
                markup.add(types.InlineKeyboardButton(file_name, callback_data=f"send_file_{file_name}"))
            
            markup.add(types.InlineKeyboardButton("BACK 🔙", callback_data="back_to_dark"))
            bot.edit_message_text(f"📍 {category} সার্ভার সিলেক্ট করুন:", 
                                 call.message.chat.id, call.message.message_id, reply_markup=markup)
        
        # নেটমড অল প্যাক
        elif call.data == "nm_all_pack":
            markup = types.InlineKeyboardMarkup(row_width=1)
            
            for country in ["BD🇧🇩", "SG🇸🇬", "IN🇮🇳"]:
                file_name = f"All Pack-{country}.nm"
                markup.add(types.InlineKeyboardButton(file_name, callback_data=f"send_file_{file_name}"))
            
            markup.add(types.InlineKeyboardButton("BACK 🔙", callback_data="back_to_netmod"))
            bot.edit_message_text("📍 All Pack সার্ভার সিলেক্ট করুন:", 
                                 call.message.chat.id, call.message.message_id, reply_markup=markup)
        
        # নেটমড ইনফো
        elif call.data == "nm_info":
            info = (
                "✅ Robi 219 TK (50GB)\n"
                "✅ Airtel Streaming (120GB)\n"
                "✅ Airtel 200 TK Social (50GB)\n"
                "✅ RYZE 297 TK (Unlimited) 💥\n"
                "✅ Stream Package All Sim 💥\n"
                "✅ Ott Package All Sim 💥\n"
                "✅ Social Package All Sim 💥\n"
                "🌍 Server: BD 🇧🇩 | SG 🇸🇬 | IN 🇮🇳"
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("BACK 🔙", callback_data="back_to_netmod"))
            bot.edit_message_text(info, call.message.chat.id, call.message.message_id, reply_markup=markup)
        
        # ফাইল পাঠান
        elif call.data.startswith('send_file_'):
            file_name = call.data.replace("send_file_", "")
            current_links = load_links()
            file_url = current_links.get(file_name)
            
            if file_url and "http" in file_url:
                try:
                    bot.send_document(call.message.chat.id, file_url, caption=f"📄 Config: {file_name}")
                except Exception as e:
                    bot.send_message(call.message.chat.id, f"❌ ফাইল পাঠানো যায়নি: {e}")
            else:
                bot.answer_callback_query(call.id, "⚠️ ফাইলটি বর্তমানে সার্ভারে নেই।", show_alert=True)
    
    except Exception as e:
        logger.error(f"কলব্যাক হ্যান্ডলারে এরর: {e}")
        bot.answer_callback_query(call.id, f"❌ এরর: {str(e)[:50]}", show_alert=True)

def process_update_link(message, file_name):
    """লিঙ্ক আপডেট প্রসেস করুন"""
    new_url = message.text.strip()
    
    if "http" not in new_url:
        bot.send_message(message.chat.id, "❌ ভুল লিঙ্ক! URL টি 'http' দিয়ে শুরু হতে হবে।")
        return
    
    try:
        current_links = load_links()
        current_links[file_name] = new_url
        save_links(current_links)
        
        with data_lock:
            global FILE_LINKS
            FILE_LINKS = current_links
        
        bot.send_message(message.chat.id, f"✅ সফলভাবে আপডেট হয়েছে!\n📂 ফাইল: `{file_name}`", 
                        parse_mode="Markdown")
    except Exception as e:
        logger.error(f"লিঙ্ক আপডেটে এরর: {e}")
        bot.send_message(message.chat.id, f"❌ এরর: {e}")

# ==================== MAIN ====================

if __name__ == "__main__":
    try:
        logger.info("বট শুরু হচ্ছে...")
        keep_alive()
        bot.infinity_polling()
    except KeyboardInterrupt:
        logger.info("বট বন্ধ হয়েছে")
    except Exception as e:
        logger.error(f"মারাত্মক এরর: {e}")