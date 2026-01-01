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

from tarot_data import TAROT_CARDS, get_tarot_interpretation, get_card_by_id
from flex_templates import (
    create_main_menu,
    create_reading_menu,
    create_card_display,
    create_spread_result,
    create_history_view,
    create_learning_menu,
    create_card_gallery,
    create_beginner_guide,
    create_celtic_cross_result,
    create_stats_view,
    create_daily_tips,
    create_search_results
)

# --------------------------------------------------
# Flask + LINE setup
# --------------------------------------------------
app = Flask(__name__)

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "YOUR_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "YOUR_CHANNEL_ACCESS_TOKEN")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# --------------------------------------------------
# تخزين مؤقت (للتطوير)
# --------------------------------------------------
user_sessions = {}
reading_history = {}
user_progress = {}
user_favorites = {}

# --------------------------------------------------
# Webhook
# --------------------------------------------------
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
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

        if text in ["بداية", "القائمة", "menu", "start"]:
            initialize_user(user_id)
            flex = FlexMessage(
                alt_text="القائمة الرئيسية",
                contents=FlexContainer.from_dict(create_main_menu())
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(event.reply_token, [flex])
            )

        elif text.startswith("بحث:"):
            term = text.split(":", 1)[1].strip()
            results = search_cards(term)

            if results:
                flex = FlexMessage(
                    alt_text="نتائج البحث",
                    contents=FlexContainer.from_dict(
                        create_search_results(results, term)
                    )
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(event.reply_token, [flex])
                )
            else:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        event.reply_token,
                        [TextMessage(text="❌ لا توجد نتائج")]
                    )
                )

        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    event.reply_token,
                    [TextMessage(
                        text="🌙 اكتب (بداية) لفتح القائمة\n🔍 بحث: اسم البطاقة"
                    )]
                )
            )

# --------------------------------------------------
# Postback
# --------------------------------------------------
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if data == "action=main_menu":
            flex = FlexMessage(
                alt_text="القائمة الرئيسية",
                contents=FlexContainer.from_dict(create_main_menu())
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(event.reply_token, [flex])
            )

        elif data == "action=reading_menu":
            flex = FlexMessage(
                alt_text="اختر نوع القراءة",
                contents=FlexContainer.from_dict(create_reading_menu())
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(event.reply_token, [flex])
            )

        elif data.startswith("action=reading&type="):
            reading_type = data.split("=")[-1]
            result = perform_reading(user_id, reading_type)

            flex = FlexMessage(
                alt_text=result["title"],
                contents=FlexContainer.from_dict(
                    create_celtic_cross_result(result)
                    if reading_type == "celtic_cross"
                    else create_spread_result(result)
                )
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(event.reply_token, [flex])
            )

        elif data == "action=daily_card":
            card = get_daily_card(user_id)
            flex = FlexMessage(
                alt_text="بطاقة اليوم",
                contents=FlexContainer.from_dict(
                    create_card_display(card, is_daily=True)
                )
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(event.reply_token, [flex])
            )

        elif data == "action=stats":
            stats = get_user_stats(user_id)
            flex = FlexMessage(
                alt_text="إحصائياتك",
                contents=FlexContainer.from_dict(
                    create_stats_view(stats)
                )
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(event.reply_token, [flex])
            )

# --------------------------------------------------
# Logic
# --------------------------------------------------
def initialize_user(user_id):
    if user_id not in user_progress:
        user_progress[user_id] = {
            "readings_count": 0,
            "cards_viewed": 0,
            "daily_cards_count": 0,
            "joined_date": datetime.now().isoformat()
        }

def perform_reading(user_id, reading_type):
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

    result = {
        "type": reading_type,
        "cards": selected,
        "timestamp": datetime.now().isoformat(),
        "interpretation": get_tarot_interpretation(reading_type, selected),
        "title": "قراءة التاروت"
    }

    reading_history.setdefault(user_id, []).insert(0, result)
    reading_history[user_id] = reading_history[user_id][:20]

    user_progress[user_id]["readings_count"] += 1
    return result

def get_daily_card(user_id):
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

    return user_sessions[user_id]["card"]

def get_user_stats(user_id):
    stats = user_progress.get(user_id)
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
    return stats

def search_cards(term):
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
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
