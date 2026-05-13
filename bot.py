import telebot
import sqlite3
import os
import google.generativeai as genai

# ✅ YE DETAILS RENDER.COM KI SETTINGS SE AAYEGI
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "")

bot = telebot.TeleBot(BOT_TOKEN)

# Gemini AI Setup
genai.configure(api_key=GEMINI_API_KEY)

# --- Database Setup ---
conn = sqlite3.connect('botmaker.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, language TEXT)')
conn.commit()

# --- Language Dictionary ---
LANGS = {
    'en': {
        'welcome': "Welcome to AI Bot Maker! 🤖\nPlease join our channel to use this bot.",
        'join_btn': "Join Channel 📢",
        'verify_btn': "Verify ✅",
        'not_joined': "❌ You haven't joined the channel yet. Please join first!",
        'dashboard': "🎉 Verified! Welcome to the AI Dashboard.\nWhat do you want to create?",
        'make_bot': "🤖 Make Bot",
        'support': "🛠 Support",
        'language': "🌐 Language",
        'ask_prompt': "Tell me, what kind of bot do you want to make? (e.g., 'A tag all bot', 'A music bot', 'A chatbot'):",
        'generating': "⏳ Generating your bot code... Please wait!",
        'hosting_guide': (
            "📖 How to Host this Bot for FREE:\n\n"
            "1. Copy the code above and save it in a file named bot.py\n"
            "2. Create another file named requirements.txt and write pyTelegramBotAPI inside it.\n"
            "3. Upload both files to a GitHub repository.\n"
            "4. Go to Render.com and log in with GitHub.\n"
            "5. Click New + and select Web Service.\n"
            "6. Connect your GitHub repo.\n"
            "7. Set Start Command to: python bot.py\n"
            "8. In the Environment section, add your BOT_TOKEN from @BotFather.\n"
            "9. Click Create Web Service and your bot will be online 24/7!"
        ),
        'select_lang': "Select your language / भाषा का चयन करें:",
        'lang_changed': "✅ Language changed successfully!"
    },
    'hi': {
        'welcome': "AI बॉट मेकर में आपका स्वागत है! 🤖\nकृपया इस बॉट का उपयोग करने के लिए चैनल जॉइन करें।",
        'join_btn': "चैनल जॉइन करें 📢",
        'verify_btn': "वेरीफाई करें ✅",
        'not_joined': "❌ आपने अभी तक चैनल जॉइन नहीं किया है। कृपया पहले जॉइन करें!",
        'dashboard': "🎉 वेरीफाइड! AI डैशबोर्ड में आपका स्वागत है।\nआप क्या बनाना चाहते हैं?",
        'make_bot': "🤖 बॉट बनाएं",
        'support': "🛠 सहायता",
        'language': "🌐 भाषा",
        'ask_prompt': "बताइए, आप कैसा बॉट बनाना चाहते हैं? (उदाहरण: 'टैग ऑल बॉट', 'म्यूजिक बॉट', 'चैटबॉट'):",
        'generating': "⏳ आपके बॉट का कोड जनरेट हो रहा है... कृपया प्रतीक्षा करें!",
        'hosting_guide': (
            "📖 इस बॉट को मुफ्त में कैसे होस्ट करें:\n\n"
            "1. ऊपर दिया गया कोड कॉपी करें और उसे bot.py नामक फ़ाइल में सेव करें।\n"
            "2. एक और फ़ाइल requirements.txt बनाएं और उसमें pyTelegramBotAPI लिखें।\n"
            "3. दोनों फ़ाइलों को GitHub रिपोजिटरी में अपलोड करें।\n"
            "4. Render.com पर जाएं और GitHub से लॉग इन करें।\n"
            "5. New + पर क्लिक करें और Web Service चुनें।\n"
            "6. अपनी GitHub रेपो कनेक्ट करें।\n"
            "7. Start Command में ये लिखें: python bot.py\n"
            "8. Environment सेक्शन में अपना BOT_TOKEN (@BotFather से लिया हुआ) डालें।\n"
            "9. Create Web Service पर क्लिक करें और आपका बॉट 24/7 ऑनलाइन हो जाएगा!"
        ),
        'select_lang': "अपनी भाषा चुनें:",
        'lang_changed': "✅ भाषा सफलतापूर्वक बदली गई!"
    },
    'zh': {
        'welcome': "欢迎来到 AI 机器人制造商！ 🤖\n请加入我们的频道以使用此机器人。",
        'join_btn': "加入频道 📢",
        'verify_btn': "验证 ✅",
        'not_joined': "❌ 您尚未加入频道。请先加入！",
        'dashboard': "🎉 已验证！欢迎来到 AI 仪表板。\n您想创建什么？",
        'make_bot': "🤖 制作机器人",
        'support': "🛠 支持",
        'language': "🌐 语言",
        'ask_prompt': "告诉我，您想制作什么样的机器人？（例如：'标记所有机器人'、'音乐机器人'）：",
        'generating': "⏳ 正在生成您的机器人代码...请稍候！",
        'hosting_guide': "📖 如何免费托管此机器人：\n1. 复制上面的代码并将其保存在名为 bot.py 的文件中。\n2. 创建另一个名为 requirements.txt 的文件，并在其中写入 pyTelegramBotAPI。\n3. 将这两个文件上传到 GitHub 仓库。\n4. 前往 Render.com 并使用 GitHub 登录。\n5. 点击 New + 并选择 Web Service。\n6. 连接您的 GitHub 仓库。\n7. 将启动命令设置为：python bot.py\n8. 在 Environment 部分中，添加来自 @BotFather 的 BOT_TOKEN。\n9. 点击 Create Web Service，您的机器人将全天候在线！",
        'select_lang': "选择您的语言：",
        'lang_changed': "✅ 语言更改成功！"
    },
    'sa': {
        'welcome': "AI बॉट निर्माता मध्ये स्वागतम्! 🤖\nकृपया वाहिनीं योजयन्तु।",
        'join_btn': "वाहिनीं योजयन्तु 📢",
        'verify_btn': "प्रमाणीकुरुते ✅",
        'not_joined': "❌ भवान् वाहिनीं न योजितवान्। प्रथमं योजयतु!",
        'dashboard': "🎉 प्रमाणीकृतम्! AI डैशबोर्ड् मध्ये स्वागतम्।\nभवान् किं निर्मातुम् इच्छति?",
        'make_bot': "🤖 बॉट निर्माण",
        'support': "🛠 सहायता",
        'language': "🌐 भाषा",
        'ask_prompt': "मम वदतु, भवान् कीदृशं बॉट निर्मातुम् इच्छति?",
        'generating': "⏳ भवतः बॉट संहिता उत्पाद्यते... कृपया प्रतीक्षतु!",
        'hosting_guide': "📖 एषः बॉट मुक्ततया कथं होस्ट् करणीयः：\n1. उपरित्य संहिता प्रतिलिख्य bot.py इति नाम्नि सञ्चिकायां रक्षतु।\n2. requirements.txt इति अन्यां सञ्चिकां निर्माय तत्र pyTelegramBotAPI लिखतु।\n3. उभे सञ्चिके GitHub इत्यत्र अपलोड् कुरुत।\n4. Render.com इत्यत्र गत्वा GitHub इत्यनेन प्रविशतु।",
        'select_lang': "भाषां चिनोतु:",
        'lang_changed': "✅ भाषा परिवर्तिता!"
    }
}

def get_language(user_id):
    cursor.execute('SELECT language FROM users WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute('INSERT INTO users (user_id, language) VALUES (?, ?)', (user_id, 'en'))
        conn.commit()
        return 'en'
    return result[0]

def set_language(user_id, lang):
    cursor.execute('UPDATE users SET language=? WHERE user_id=?', (lang, user_id))
    conn.commit()

def get_text(user_id, key):
    lang = get_language(user_id)
    return LANGS[lang].get(key, LANGS['en'][key])

def check_join(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# ✅ FIX: Long messages ko automatically split karne ka function
def send_long_message(chat_id, text):
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            bot.send_message(chat_id, text[x:x+4096])
    else:
        bot.send_message(chat_id, text)

# --- Dashboard & Menus ---
def show_dashboard(message):
    user_id = message.chat.id
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(get_text(user_id, 'make_bot'), callback_data="make_bot"))
    markup.add(
        telebot.types.InlineKeyboardButton(get_text(user_id, 'support'), url="https://t.me/Winy_x"),
        telebot.types.InlineKeyboardButton(get_text(user_id, 'language'), callback_data="lang_menu")
    )
    bot.send_message(user_id, get_text(user_id, 'dashboard'), reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if check_join(user_id):
        show_dashboard(message)
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(get_text(user_id, 'join_btn'), url=CHANNEL_LINK))
        markup.add(telebot.types.InlineKeyboardButton(get_text(user_id, 'verify_btn'), callback_data="verify"))
        bot.send_message(user_id, get_text(user_id, 'welcome'), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if check_join(call.from_user.id):
        show_dashboard(call.message)
    else:
        bot.answer_callback_query(call.id, get_text(call.from_user.id, 'not_joined'), show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "lang_menu")
def lang_menu(call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("English 🇬🇧", callback_data="lang_en"),
        telebot.types.InlineKeyboardButton("Hindi 🇮🇳", callback_data="lang_hi")
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Chinese 🇨🇳", callback_data="lang_zh"),
        telebot.types.InlineKeyboardButton("Sanskrit 🕉️", callback_data="lang_sa")
    )
    bot.edit_message_text(get_text(call.from_user.id, 'select_lang'), call.from_user.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def change_lang(call):
    lang = call.data.split("_")[1]
    set_language(call.from_user.id, lang)
    bot.answer_callback_query(call.id, get_text(call.from_user.id, 'lang_changed'), show_alert=True)
    show_dashboard(call.message)

# --- CODE GENERATION LOGIC ---
@bot.callback_query_handler(func=lambda call: call.data == "make_bot")
def make_bot(call):
    user_id = call.from_user.id
    msg = bot.send_message(user_id, get_text(user_id, 'ask_prompt'))
    bot.register_next_step_handler(msg, process_prompt_step)

def process_prompt_step(message):
    user_id = message.from_user.id
    prompt = message.text
    
    wait_msg = bot.send_message(user_id, get_text(user_id, 'generating'))
    
    try:
        generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "max_output_tokens": 4096,
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="You are an expert Telegram bot developer. Write a complete, working Python script using the pyTelegramBotAPI library for the requested bot. Output ONLY the Python code inside a python code block. Do not add extra text outside the code block. Use BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE' for the token."
        )
        
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        
        # Delete the "Generating..." message
        bot.delete_message(user_id, wait_msg.message_id)
        
        # ✅ FIX: Use send_long_message instead of bot.send_message to avoid length errors
        send_long_message(user_id, response.text)
        
        # Send the Hosting Guide (without Markdown parse mode to avoid formatting errors)
        bot.send_message(user_id, get_text(user_id, 'hosting_guide'))
        
    except Exception as e:
        bot.delete_message(user_id, wait_msg.message_id)
        bot.send_message(user_id, f"❌ Error generating code. Please check your API Key or try again.\nError: {str(e)}")

if __name__ == "__main__":
    print("Bot Code Generator is running...")
    bot.infinity_polling()
