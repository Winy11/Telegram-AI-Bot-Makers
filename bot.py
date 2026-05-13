import telebot
import threading
import sqlite3
import os
import google.generativeai as genai

# ✅ AB YAHAN KUCH NAHI LIKHNA HAI! YE DETAILS RENDER.COM KI SETTINGS SE AAYEGI
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
cursor.execute('CREATE TABLE IF NOT EXISTS bots (token TEXT PRIMARY KEY, owner_id INTEGER, prompt TEXT)')
conn.commit()

# --- Language Dictionary ---
LANGS = {
    'en': {
        'welcome': "Welcome to AI Bot Maker! 🤖\nPlease join our channel to use this bot.",
        'join_btn': "Join Channel 📢",
        'verify_btn': "Verify ✅",
        'not_joined': "❌ You haven't joined the channel yet. Please join first!",
        'dashboard': "🎉 Verified! Welcome to the AI Dashboard.\nWhat do you want to create?",
        'make_bot': "🤖 Make AI Bot",
        'support': "🛠 Support",
        'language': "🌐 Language",
        'ask_token': "Step 1: Send me the Bot Token (from @BotFather) for your new AI bot:",
        'ask_prompt': "Step 2: Great! Now tell me, what should this bot do? (e.g., 'Act as a rude comedian', 'Act as a Python expert', 'Talk like a gangster'):",
        'invalid_token': "❌ Invalid Token. Please send a correct token from @BotFather.",
        'bot_success': "✅ Your AI Bot is now online and ready! It will behave exactly as you described.",
        'select_lang': "Select your language / भाषा का चयन करें:",
        'lang_changed': "✅ Language changed successfully!"
    },
    'hi': {
        'welcome': "AI बॉट मेकर में आपका स्वागत है! 🤖\nकृपया इस बॉट का उपयोग करने के लिए चैनल जॉइन करें।",
        'join_btn': "चैनल जॉइन करें 📢",
        'verify_btn': "वेरीफाई करें ✅",
        'not_joined': "❌ आपने अभी तक चैनल जॉइन नहीं किया है। कृपया पहले जॉइन करें!",
        'dashboard': "🎉 वेरीफाइड! AI डैशबोर्ड में आपका स्वागत है।\nआप क्या बनाना चाहते हैं?",
        'make_bot': "🤖 AI बॉट बनाएं",
        'support': "🛠 सहायता",
        'language': "🌐 भाषा",
        'ask_token': "चरण 1: मुझे अपने नए AI बॉट का टोकन (@BotFather से) भेजें:",
        'ask_prompt': "चरण 2: बहुत बढ़िया! अब मुझे बताएं, यह बॉट क्या करेगा? (उदाहरण: 'एक गुस्सैल कॉमेडियन की तरह बात करो', 'पायथन एक्सपर्ट बनो'):",
        'invalid_token': "❌ अमान्य टोकन। कृपया सही टोकन भेजें।",
        'bot_success': "✅ आपका AI बॉट अब ऑनलाइन है! यह बिल्कुल वैसा ही बोलेगा जैसा आपने बताया।",
        'select_lang': "अपनी भाषा चुनें:",
        'lang_changed': "✅ भाषा सफलतापूर्वक बदली गई!"
    },
    'zh': {
        'welcome': "欢迎来到 AI 机器人制造商！ 🤖\n请加入我们的频道以使用此机器人。",
        'join_btn': "加入频道 📢",
        'verify_btn': "验证 ✅",
        'not_joined': "❌ 您尚未加入频道。请先加入！",
        'dashboard': "🎉 已验证！欢迎来到 AI 仪表板。\n您想创建什么？",
        'make_bot': "🤖 制作 AI 机器人",
        'support': "🛠 支持",
        'language': "🌐 语言",
        'ask_token': "步骤 1：向我发送新 AI 机器人的令牌（来自 @BotFather）：",
        'ask_prompt': "步骤 2：太好了！现在告诉我，这个机器人应该做什么？",
        'invalid_token': "❌ 无效令牌。请发送正确的令牌。",
        'bot_success': "✅ 您的 AI 机器人现已上线并准备就绪！",
        'select_lang': "选择您的语言：",
        'lang_changed': "✅ 语言更改成功！"
    },
    'sa': {
        'welcome': "AI बॉट निर्माता मध्ये स्वागतम्! 🤖\nकृपया वाहिनीं योजयन्तु।",
        'join_btn': "वाहिनीं योजयन्तु 📢",
        'verify_btn': "प्रमाणीकुरुते ✅",
        'not_joined': "❌ भवान् वाहिनीं न योजितवान्। प्रथमं योजयतु!",
        'dashboard': "🎉 प्रमाणीकृतम्! AI डैशबोर्ड् मध्ये स्वागतम्।\nभवान् किं निर्मातुम् इच्छति?",
        'make_bot': "🤖 AI बॉट निर्माण",
        'support': "🛠 सहायता",
        'language': "🌐 भाषा",
        'ask_token': "चरणम् १: मम नूतन AI बॉट टोकन प्रेषयन्तु:",
        'ask_prompt': "चरणम् २: अद्यतन! अधुना मम वदतु, एषः बॉट किं करिष्यति?",
        'invalid_token': "❌ अमान्यं टोकन।",
        'bot_success': "✅ भवतः AI बॉट अद्यावधि अनलाइन् अस्ति!",
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

# --- AI BOT MAKING LOGIC ---
@bot.callback_query_handler(func=lambda call: call.data == "make_bot")
def make_bot(call):
    user_id = call.from_user.id
    msg = bot.send_message(user_id, get_text(user_id, 'ask_token'))
    bot.register_next_step_handler(msg, process_token_step)

def process_token_step(message):
    user_id = message.from_user.id
    token = message.text
    
    try:
        test_bot = telebot.TeleBot(token)
        test_bot.get_me()
        
        msg = bot.send_message(user_id, get_text(user_id, 'ask_prompt'))
        bot.register_next_step_handler(msg, process_prompt_step, token)
        
    except Exception:
        bot.send_message(user_id, get_text(user_id, 'invalid_token'))

def process_prompt_step(message, token):
    user_id = message.from_user.id
    prompt = message.text
    
    cursor.execute('INSERT INTO bots (token, owner_id, prompt) VALUES (?, ?, ?)', (token, user_id, prompt))
    conn.commit()
    
    bot.send_message(user_id, get_text(user_id, 'bot_success'))
    
    start_ai_sub_bot(token, prompt)

def start_ai_sub_bot(token, system_prompt):
    sub_bot = telebot.TeleBot(token)
    
    # ✅ AUTOMATICALLY UPDATE BOT BIO (ABOUT)
    try:
        sub_bot.set_my_description(description="Host & Make Your Bot Free via @BotCreatorsBot")
        sub_bot.set_my_short_description(short_description="Host & Make Your Bot Free via @BotCreatorsBot")
    except Exception as e:
        print(f"Could not update bio: {e}")
    
    # Gemini AI Setup for Sub-Bot
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "max_output_tokens": 2048,
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=system_prompt
    )
    
    @sub_bot.message_handler(commands=['start'])
    def sub_start(message):
        sub_bot.reply_to(message, "Hello! I am ready. Ask me anything!")
        
    @sub_bot.message_handler(func=lambda m: True)
    def sub_chat(message):
        try:
            chat = model.start_chat(history=[])
            response = chat.send_message(message.text)
            ai_reply = response.text
            sub_bot.reply_to(message, ai_reply)
        except Exception as e:
            sub_bot.reply_to(message, "Error generating response.")

    thread = threading.Thread(target=sub_bot.infinity_polling)
    thread.start()

def load_existing_bots():
    cursor.execute('SELECT token, prompt FROM bots')
    bots = cursor.fetchall()
    for b_token, b_prompt in bots:
        start_ai_sub_bot(b_token, b_prompt)

if __name__ == "__main__":
    print("Starting Bot Maker & Loading Created Bots...")
    load_existing_bots()
    bot.infinity_polling()
