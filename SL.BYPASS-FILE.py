import telebot
from telebot import types
import os
import json
from datetime import datetime

# আপনার বটের টোকেন
API_TOKEN = '8247492389:AAGXmHZRXV1KPXF-wrPgXZ7mctBsH5Dse1g'
bot = telebot.TeleBot(API_TOKEN)

CHANNELS = ['-1002779233092'] 
LINK = "https://t.me/+CifzqwitOghlMDk9"
ADMIN_USERNAME = "@SL_BORSHON"
ADMIN_ID = 5755517737  
USER_FILE = "users.txt"
USER_DATA_FILE = "user_details.txt"
LINKS_JSON = "file_links.json"

# ডিফল্ট লিঙ্ক ডিকশনারি
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

def load_links():
    if os.path.exists(LINKS_JSON):
        try:
            with open(LINKS_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_LINKS
    return DEFAULT_LINKS

def save_links(links):
    with open(LINKS_JSON, "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=4)

# গ্লোবাল ডাটা স্টোর
FILE_LINKS = load_links()
pending_data = {}

def save_user(user):
    user_id = str(user.id)
    first_name = user.first_name if user.first_name else "User"
    username = f"@{user.username}" if user.username else "N/A"
    
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", encoding="utf-8") as f: pass
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", encoding="utf-8") as f: pass

    with open(USER_FILE, "r", encoding="utf-8") as f:
        users = f.read().splitlines()
    
    if user_id not in users:
        with open(USER_FILE, "a", encoding="utf-8") as f:
            f.write(user_id + "\n")
        with open(USER_DATA_FILE, "a", encoding="utf-8") as f:
            f.write(f"Name: {first_name} | User: {username} | ID: {user_id}\n")
        notify_admin_new_user(user, len(users) + 1)

def notify_admin_new_user(user, total_users):
    now = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    caption = (
        f"📊 **নতুন ইউজারের বিস্তারিত তথ্য**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 **নাম:** {user.first_name}\n"
        f"🆔 **আইডি:** `{user.id}`\n"
        f"🏷️ **ইউজারনেম:** @{user.username if user.username else 'N/A'}\n"
        f"🌐 **ল্যাঙ্গুয়েজ:** {user.language_code}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📈 **বটের মোট ইউজার:** {total_users}\n"
        f"⏰ **সময়:** {now} (BD)"
    )
    try:
        photos = bot.get_user_profile_photos(user.id)
        if photos.total_count > 0:
            bot.send_photo(ADMIN_ID, photos.photos[0][-1].file_id, caption=caption, parse_mode="Markdown")
        else:
            bot.send_message(ADMIN_ID, caption, parse_mode="Markdown")
    except:
        bot.send_message(ADMIN_ID, caption, parse_mode="Markdown")

def check_join(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status in ['left', 'kicked']: return False
        except: return False
    return True

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("DARK TUNNEL 🔑", "NETMOD VPN 🔑", "SUPPORT ☎️", "অভিযোগ 📝")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user)
    if check_join(message.from_user.id):
        bot.send_message(message.chat.id, "🎉 স্বাগতম! আপনার প্রয়োজনীয় অপশনটি বেছে নিন।", reply_markup=main_menu())
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 জয়েন করুন", url=LINK))
        markup.add(types.InlineKeyboardButton("✅ ভেরিফাই করুন", callback_data="verify_join"))
        bot.send_message(message.chat.id, "⚠️ আগে চ্যানেলে জয়েন করুন।", reply_markup=markup)

@bot.message_handler(commands=['update'])
def update_link_cmd(message):
    if message.from_user.id == ADMIN_ID:
        markup = types.InlineKeyboardMarkup(row_width=1)
        current_links = load_links()
        for file_name in current_links.keys():
            markup.add(types.InlineKeyboardButton(f"Update: {file_name}", callback_data=f"up_req_{file_name}"))
        bot.send_message(message.chat.id, "⚙️ আপনি কোন ফাইলটির লিঙ্ক পরিবর্তন করতে চান?", reply_markup=markup)
    else:
        bot.reply_to(message, "❌ আপনি অ্যাডমিন নন।")

@bot.message_handler(commands=['User-List'])
def user_list_cmd(message):
    if message.from_user.id == ADMIN_ID:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r", encoding="utf-8") as f: data = f.read()
            if data:
                if len(data) > 4000:
                    with open(USER_DATA_FILE, "rb") as f: bot.send_document(message.chat.id, f, caption="📜 সম্পূর্ণ ইউজার লিস্ট")
                else: bot.send_message(message.chat.id, f"📜 **ইউজার লিস্ট:**\n\n{data}", parse_mode="Markdown")
            else: bot.send_message(message.chat.id, "এখনো কোনো ইউজার নেই।")
        else: bot.send_message(message.chat.id, "ইউজার ফাইলটি খুঁজে পাওয়া যায়নি।")

@bot.message_handler(commands=['Admin-News'])
def admin_news_cmd(message):
    if message.from_user.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "📝 সবাইকে পাঠানোর জন্য আপনার নিউজ মেসেজটি লিখুন (Text/Photo/Video):")
        bot.register_next_step_handler(msg, process_broadcast_step)

def process_broadcast_step(message):
    pending_data['news_msg'] = message
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ হ্যাঁ, পাঠান", callback_data="send_news"),
               types.InlineKeyboardButton("❌ বাতিল", callback_data="cancel_news"))
    bot.send_message(message.chat.id, "⚠️ আপনি কি নিশ্চিত যে এই মেসেজটি সকল ইউজারকে পাঠাতে চান?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "অভিযোগ 📝")
def complaint_start(message):
    msg = bot.send_message(message.chat.id, "✍️ আপনার অভিযোগটি বিস্তারিত লিখুন:")
    bot.register_next_step_handler(msg, process_complaint_step)

def process_complaint_step(message):
    user_id = message.from_user.id
    pending_data[user_id] = message.text
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ হ্যাঁ, পাঠান", callback_data="send_comp"),
               types.InlineKeyboardButton("❌ বাতিল", callback_data="cancel_comp"))
    bot.send_message(message.chat.id, f"⚠️ আপনি কি নিশ্চিত যে এই অভিযোগটি অ্যাডমিনের কাছে পাঠাতে চান?\n\n`{message.text}`", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "SUPPORT ☎️")
def support_handler(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📨 কন্টাক্ট অ্যাডমিন", url=f"https://t.me/{ADMIN_USERNAME.replace('@','')}"))
    bot.send_message(message.chat.id, f"যোগাযোগ করতে নিচের বাটনে ক্লিক করুন।", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_all(call):
    user_id = call.from_user.id

    if call.data == "send_comp":
        complaint_text = pending_data.get(user_id)
        if complaint_text:
            bot.send_message(ADMIN_ID, f"📩 **নতুন অভিযোগ!**\n\nইউজার: {call.from_user.first_name} (@{call.from_user.username})\n🆔 আইডি: `{user_id}`\n\n📝 অভিযোগ: {complaint_text}", parse_mode="Markdown")
            bot.edit_message_text("✅ আপনার অভিযোগটি অ্যাডমিনের কাছে সফলভাবে পাঠানো হয়েছে।", call.message.chat.id, call.message.message_id)
            del pending_data[user_id]
    
    elif call.data == "cancel_comp":
        if user_id in pending_data: del pending_data[user_id]
        bot.edit_message_text("❌ অভিযোগ বাতিল করা হয়েছে।", call.message.chat.id, call.message.message_id)

    elif call.data == "send_news":
        original_msg = pending_data.get('news_msg')
        if original_msg and os.path.exists(USER_FILE):
            with open(USER_FILE, "r", encoding="utf-8") as f: users = f.read().splitlines()
            count = 0
            bot.edit_message_text("⏳ ব্রডকাস্ট শুরু হয়েছে...", call.message.chat.id, call.message.message_id)
            for u in users:
                try: 
                    bot.copy_message(u, original_msg.chat.id, original_msg.message_id)
                    count += 1
                except: continue
            bot.send_message(call.message.chat.id, f"✅ নিউজ সফলভাবে {count} জন ইউজারের কাছে পাঠানো হয়েছে।")
            if 'news_msg' in pending_data: del pending_data['news_msg']

    elif call.data == "cancel_news":
        if 'news_msg' in pending_data: del pending_data['news_msg']
        bot.edit_message_text("❌ নিউজ ব্রডকাস্ট বাতিল করা হয়েছে।", call.message.chat.id, call.message.message_id)

    elif call.data == "verify_join":
        if check_join(user_id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "✅ ভেরিফিকেশন সফল!", reply_markup=main_menu())
        else: bot.answer_callback_query(call.id, "❌ জয়েন করেননি!", show_alert=True)

    elif call.data == "back_to_dark":
        dark_tunnel_menu(call.message, is_edit=True)
    
    elif call.data == "back_to_netmod":
        netmod_vpn_menu(call.message, is_edit=True)

    elif call.data.startswith('up_req_'):
        file_to_update = call.data.replace("up_req_", "")
        msg = bot.send_message(call.message.chat.id, f"🔗 `{file_to_update}` এর জন্য নতুন লিঙ্কটি পাঠান:", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_update_link, file_to_update)

    elif call.data.startswith('dt_'):
        category = call.data.replace("dt_", "")
        markup = types.InlineKeyboardMarkup(row_width=1)
        for c in ["BD🇧🇩", "SG🇸🇬", "IN🇮🇳"]:
            file_name = f"{category}-{c}.dark"
            markup.add(types.InlineKeyboardButton(file_name, callback_data=f"send_file_{file_name}"))
        markup.add(types.InlineKeyboardButton("BACK 🔙", callback_data="back_to_dark"))
        bot.edit_message_text(f"📍 {category} সার্ভার সিলেক্ট করুন:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "nm_all_pack":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for c in ["BD🇧🇩", "SG🇸🇬", "IN🇮🇳"]:
            file_name = f"All Pack-{c}.nm"
            markup.add(types.InlineKeyboardButton(file_name, callback_data=f"send_file_{file_name}"))
        markup.add(types.InlineKeyboardButton("BACK 🔙", callback_data="back_to_netmod"))
        bot.edit_message_text("📍 All Pack সার্ভার সিলেক্ট করুন:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "nm_info":
        info = "✅ Robi 219 TK (50GB)\n✅ Airtel Streaming (120GB)\n✅ Airtel 200 TK Social (50GB)\n✅ RYZE 297 TK (Unlimited) 💥\n✅ Stream Package All Sim 💥\n✅ Ott Package All Sim 💥\n✅ Social Package All Sim 💥\n🌍 Server: BD 🇧🇩 | SG 🇸🇬 | IN 🇮🇳"
        markup = types.InlineKeyboardMarkup(); markup.add(types.InlineKeyboardButton("BACK 🔙", callback_data="back_to_netmod"))
        bot.edit_message_text(info, call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith('send_file_'):
        file_name = call.data.replace("send_file_", "")
        current_links = load_links()
        file_url = current_links.get(file_name)
        if file_url and "http" in file_url:
            try: 
                # আপনার রিকোয়েস্ট অনুযায়ী send_document মেথডই রাখা হয়েছে
                bot.send_document(call.message.chat.id, file_url, caption=f"📄 Config: {file_name}")
            except Exception as e: 
                bot.send_message(call.message.chat.id, f"❌ ফাইল পাঠানো যায়নি।\nকারণ: লিঙ্কটি টেলিগ্রাম ফাইল লিঙ্ক হতে হবে।\nভুল: {str(e)}")
        else: 
            bot.answer_callback_query(call.id, "⚠️ ফাইলটি বর্তমানে সার্ভারে নেই বা লিঙ্ক ভুল।", show_alert=True)

def process_update_link(message, file_name):
    new_url = message.text.strip()
    if "http" in new_url:
        current_links = load_links()
        current_links[file_name] = new_url
        save_links(current_links)
        bot.send_message(message.chat.id, f"✅ সফলভাবে আপডেট হয়েছে!\n\n📂 ফাইল: `{file_name}`\n🔗 নতুন লিঙ্ক: {new_url}", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ ভুল লিঙ্ক! অবশ্যই একটি ভ্যালিড URL (http/https) পাঠাতে হবে।")

@bot.message_handler(func=lambda message: message.text == "DARK TUNNEL 🔑")
def dark_tunnel_menu(message, is_edit=False):
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
    for t, d in opts: markup.add(types.InlineKeyboardButton(t, callback_data=d))
    
    if is_edit:
        bot.edit_message_text("📂 DARK TUNNEL ক্যাটাগরি সিলেক্ট করুন:", message.chat.id, message.message_id, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "📂 DARK TUNNEL ক্যাটাগরি সিলেক্ট করুন:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "NETMOD VPN 🔑")
def netmod_vpn_menu(message, is_edit=False):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("All Pack.nm 🌐", callback_data="nm_all_pack"),
               types.InlineKeyboardButton("All Pack.Info ♾️", callback_data="nm_info"))
    
    if is_edit:
        bot.edit_message_text("📂 NETMOD VPN ক্যাটাগরি সিলেক্ট করুন:", message.chat.id, message.message_id, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "📂 NETMOD VPN ক্যাটাগরি সিলেক্ট করুন:", reply_markup=markup)

if __name__ == "__main__":
    print("Bot is running with Dynamic Link Update feature...")
    bot.infinity_polling()