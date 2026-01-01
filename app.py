from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent
import os
import random
from datetime import datetime

from tarot_data import TAROT_CARDS, get_tarot_interpretation
from flex_templates import (
    create_main_menu,
    create_reading_menu,
    create_card_display,
    create_spread_result,
    create_stats_view,
    create_search_results,
    create_celtic_cross_result,
    create_learning_menu,
    create_beginner_guide
)

# --------------------------------------------------
# Flask + LINE setup
# --------------------------------------------------
app = Flask(__name__)

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_ACCESS_TOKEN:
    raise ValueError("LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN must be set")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# --------------------------------------------------
# تخزين مؤقت (في الإنتاج استخدم Redis)
# --------------------------------------------------
user_sessions = {}
reading_history = {}
user_progress = {}

# --------------------------------------------------
# Webhook
# --------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return "Tarot Bot is running!", 200

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature")
        abort(400)

    return "OK"

# --------------------------------------------------
# Text Messages
# --------------------------------------------------
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if text in ["بداية", "القائمة", "menu", "start", "Start", "القائمه"]:
            initialize_user(user_id)
            flex = FlexMessage(
                alt_text="🌙 القائمة الرئيسية",
                contents=FlexContainer.from_dict(create_main_menu())
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex]
                )
            )

        elif text.startswith("بحث:") or text.startswith("search:"):
            term = text.split(":", 1)[1].strip()
            results = search_cards(term)

            if results:
                flex = FlexMessage(
                    alt_text=f"🔍 نتائج البحث: {term}",
                    contents=FlexContainer.from_dict(
                        create_search_results(results, term)
                    )
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex]
                    )
                )
            else:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f"❌ لم نجد نتائج لـ '{term}'")]
                    )
                )

        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text="🌙 مرحباً بك في بوت التاروت!\n\n"
                             "🎴 اكتب 'بداية' أو 'menu' لفتح القائمة\n"
                             "🔍 اكتب 'بحث: اسم البطاقة' للبحث\n\n"
                             "مثال: بحث: المهرج"
                    )]
                )
            )

# --------------------------------------------------
# Postback Events
# --------------------------------------------------
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        try:
            if data == "action=main_menu":
                flex = FlexMessage(
                    alt_text="🌙 القائمة الرئيسية",
                    contents=FlexContainer.from_dict(create_main_menu())
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex]
                    )
                )

            elif data == "action=reading_menu":
                flex = FlexMessage(
                    alt_text="🎴 اختر نوع القراءة",
                    contents=FlexContainer.from_dict(create_reading_menu())
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex]
                    )
                )

            elif data.startswith("action=reading&type="):
                reading_type = data.split("=")[-1]
                result = perform_reading(user_id, reading_type)

                if reading_type == "celtic_cross":
                    flex = FlexMessage(
                        alt_text="✨ قراءة الصليب السلتي",
                        contents=FlexContainer.from_dict(
                            create_celtic_cross_result(result)
                        )
                    )
                else:
                    flex = FlexMessage(
                        alt_text=f"✨ {result['title']}",
                        contents=FlexContainer.from_dict(
                            create_spread_result(result)
                        )
                    )
                
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex]
                    )
                )

            elif data == "action=daily_card":
                card = get_daily_card(user_id)
                flex = FlexMessage(
                    alt_text="🔮 بطاقة اليوم",
                    contents=FlexContainer.from_dict(
                        create_card_display(card, is_daily=True)
                    )
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex]
                    )
                )

            elif data == "action=stats":
                stats = get_user_stats(user_id)
                flex = FlexMessage(
                    alt_text="📊 إحصائياتك",
                    contents=FlexContainer.from_dict(
                        create_stats_view(stats)
                    )
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex]
                    )
                )

            elif data == "action=learning_menu":
                flex = FlexMessage(
                    alt_text="📚 مركز التعلم",
                    contents=FlexContainer.from_dict(create_learning_menu())
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex]
                    )
                )

            elif data == "action=beginner_guide":
                flex = FlexMessage(
                    alt_text="🌱 دليل المبتدئين",
                    contents=FlexContainer.from_dict(create_beginner_guide())
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex]
                    )
                )

            elif data.startswith("action=card_detail&id="):
                card_id = int(data.split("=")[-1])
                card = next((c for c in TAROT_CARDS if c["id"] == card_id), None)
                
                if card:
                    card_copy = card.copy()
                    card_copy["reversed"] = False
                    flex = FlexMessage(
                        alt_text=f"🎴 {card['name_ar']}",
                        contents=FlexContainer.from_dict(
                            create_card_display(card_copy, is_learning=True)
                        )
                    )
                    line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[flex]
                        )
                    )

        except Exception as e:
            app.logger.error(f"Error handling postback: {e}")
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="❌ حدث خطأ، حاول مرة أخرى")]
                )
            )

# --------------------------------------------------
# Logic Functions
# --------------------------------------------------
def initialize_user(user_id):
    """تهيئة بيانات المستخدم"""
    if user_id not in user_progress:
        user_progress[user_id] = {
            "readings_count": 0,
            "cards_viewed": 0,
            "daily_cards_count": 0,
            "joined_date": datetime.now().isoformat()
        }

def perform_reading(user_id, reading_type):
    """تنفيذ قراءة التاروت"""
    cards_needed = {
        "single": 1,
        "past_present_future": 3,
        "relationship": 3,
        "decision": 2,
        "celtic_cross": 10
    }.get(reading_type, 1)

    selected = []
    for c in random.sample(TAROT_CARDS, cards_needed):
        card = c.copy()
        card["reversed"] = random.choice([True, False])
        selected.append(card)

    titles = {
        "single": "قراءة بطاقة واحدة",
        "past_present_future": "الماضي والحاضر والمستقبل",
        "relationship": "قراءة العلاقات",
        "decision": "قراءة اتخاذ القرار",
        "celtic_cross": "قراءة الصليب السلتي"
    }

    result = {
        "type": reading_type,
        "cards": selected,
        "timestamp": datetime.now().isoformat(),
        "interpretation": get_tarot_interpretation(reading_type, selected),
        "title": titles.get(reading_type, "قراءة التاروت")
    }

    # حفظ في السجل
    if user_id not in reading_history:
        reading_history[user_id] = []
    reading_history[user_id].insert(0, result)
    reading_history[user_id] = reading_history[user_id][:20]

    # تحديث الإحصائيات
    user_progress[user_id]["readings_count"] += 1
    
    return result

def get_daily_card(user_id):
    """الحصول على بطاقة اليوم"""
    today = datetime.now().strftime("%Y-%m-%d")

    if user_id not in user_sessions:
        user_sessions[user_id] = {}

    if user_sessions[user_id].get("date") != today:
        card = random.choice(TAROT_CARDS).copy()
        card["reversed"] = random.choice([True, False])
        user_sessions[user_id] = {
            "date": today,
            "card": card
        }
        user_progress[user_id]["daily_cards_count"] += 1

    return user_sessions[user_id]["card"]

def get_user_stats(user_id):
    """الحصول على إحصائيات المستخدم"""
    initialize_user(user_id)
    stats = user_progress[user_id].copy()
    
    total = (
        stats["readings_count"]
        + stats["cards_viewed"]
        + stats["daily_cards_count"]
    )

    if total < 10:
        level = "مبتدئ 🌱"
    elif total < 50:
        level = "متعلم 📚"
    elif total < 100:
        level = "متمرس ✨"
    else:
        level = "خبير 🌟"

    stats["level"] = level
    stats["total"] = total
    return stats

def search_cards(term):
    """البحث عن البطاقات"""
    term = term.lower()
    results = []

    for card in TAROT_CARDS:
        if (
            term in card["name"].lower()
            or term in card["name_ar"].lower()
            or any(term in k.lower() for k in card.get("keywords", []))
        ):
            results.append(card)

    return results[:10]

# --------------------------------------------------
# Run App
# --------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
