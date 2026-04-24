# 🤖 Telegram VPN Config Bot

বাংলাদেশে তৈরি একটি শক্তিশালী Telegram বট যা VPN কনফিগ ডিস্ট্রিবিউট করে।

## 📋 ফিচার

✅ চ্যানেল জয়েন ভেরিফিকেশন  
✅ ডার্ক টানেল কনফিগ ডাউনলোড  
✅ নেটমড ভিপিএন প্যাকেজ  
✅ অ্যাডমিন ব্রডকাস্ট সিস্টেম  
✅ ইউজার ট্র্যাকিং  
✅ লাইভ লিঙ্ক আপডেট  

## 🚀 দ্রুত শুরু করুন

### **স্টেপ ১: গিটহাব রেপোজিটরি ক্লোন করুন**
```bash
git clone https://github.com/YOUR_USERNAME/my-telegram-bot.git
cd my-telegram-bot
```

### **স্টেপ ২: ভার্চুয়াল এনভায়রনমেন্ট সেটআপ করুন**
```bash
python -m venv venv
source venv/bin/activate  # ম্যাক/লিনাক্স
venv\Scripts\activate     # ���ইন্ডোজ
```

### **স্টেপ ৩: ডিপেন্ডেন্সি ইনস্টল করুন**
```bash
pip install -r requirements.txt
```

### **স্টেপ ৪: .env ফাইল তৈরি করুন**
```bash
cp .env.example .env
```

এখন `.env` ফাইল খুলে আপনার তথ্য দিন:
```env
TELEGRAM_BOT_TOKEN=আপনার_টোকেন
ADMIN_ID=আপনার_চ্যাট_আইডি
# অন্যান্য সেটিংস...
```

### **স্টেপ ৫: লোকালি টেস্ট করুন**
```bash
python bot.py
```

---

## 🌐 Render এ ডিপ্লয় করুন

### **স্টেপ ১: গিটহাবে পুশ করুন**
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### **স্টেপ ২: Render এ অ্যাকাউন্ট তৈরি করুন**
- যান: https://render.com
- গিটহাব একাউন্ট দিয়ে সাইন আপ করুন

### **স্টেপ ৩: নতুন Web Service তৈরি করুন**
1. Dashboard → "New +" → Web Service
2. আপনার রেপোজিটরি সিলেক্ট করুন
3. সেটিংস পূরণ করুন:
   - **Name**: `telegram-bot` (যেকোনো নাম)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`

### **স্টেপ ৪: এনভায়রনমেন্ট ভেরিয়েবল যোগ করুন**
Settings → Environment → Add
```
TELEGRAM_BOT_TOKEN = আপনার_টোকেন
ADMIN_ID = আপনার_আইডি
CHANNELS = -1002779233092
CHANNEL_LINK = https://t.me/your_channel
ADMIN_USERNAME = @your_admin
```

### **স্টে��� ৫: ডিপ্লয় করুন**
"Create Web Service" ক্লিক করুন। ৫ মিনিটে বট লাইভ হবে!

---

## 🔧 অ্যাডমিন কমান্ড

```
/start          - বট শুরু করুন
/update         - লিঙ্ক আপডেট করুন
/User-List      - ইউজার লিস্ট দেখুন
/Admin-News     - সবাইকে বার্তা পাঠান
/Private-Msg    - কাউকে ব্যক্তিগত বার্তা পাঠান
```

---

## 📝 প্রয়োজনীয় তথ্য সংগ্রহ করুন

### **Telegram বট টোকেন পেতে:**
1. @BotFather সার্চ করুন
2. /newbot পাঠান
3. বটের নাম ও ইউজারনেম দিন
4. টোকেন কপি করুন

### **চ্যাট আইডি বের করতে:**
1. @userinfobot সার্চ করুন
2. মেসেজ পাঠান
3. আপনার ID দেখবেন

---

## 🐛 সমস্যা সমাধান

**Q: বট শুরু হচ্ছে না?**
A: `.env` ফাইল চেক করুন এবং টোকেন ঠিক আছে কিনা দেখুন

**Q: Render এ বট বন্ধ হয়ে যাচ্ছে?**
A: Logs দেখুন এবং error টি নোট করুন

**Q: ফাইল ডাউনলোড হচ্ছে না?**
A: `file_links.json` এ লিঙ্ক ঠিক আছে কিনা চেক করুন

---

## 📞 সাপোর্ট

যেকোনো সমস্যার জন্য Issues খুলুন।

---

## ⚖️ লাইসেন্স

MIT License