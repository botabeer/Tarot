import os
import random
import sqlite3
import logging
from datetime import datetime
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent

from tarot_data import TAROT_CARDS, get_tarot_interpretation, get_card_by_id
from flex_templates import *

# --------------------------------------------------
# إعدادات
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_ACCESS_TOKEN:
    raise RuntimeError("LINE credentials not set")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

DB_NAME = "tarot.db"

# --------------------------------------------------
# قاعدة البيانات
# --------------------------------------------------
def db():
    return sqlite3.connect(DB_NAME)

def init_db():
    with db() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            joined_date TEXT,
            last_active TEXT,
            readings INTEGER DEFAULT 0,
            cards_viewed INTEGER DEFAULT 0,
            daily_cards INTEGER DEFAULT 0
        )""")

        c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            type TEXT,
            data TEXT,
            created_at TEXT
        )""")

        c.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            user_id TEXT,
            card_id INTEGER,
            UNIQUE(user_id, card_id)
        )""")

        c.execute("""
        CREATE TABLE IF NOT EXISTS daily (
            user_id TEXT PRIMARY KEY,
            card_id INTEGER,
            reversed INTEGER,
            date TEXT
        )""")

init_db()

# --------------------------------------------------
# أدوات مساعدة
# --------------------------------------------------
def reply(event, messages):
    with ApiClient(configuration) as api_client:
        MessagingApi(api_client).reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages if isinstance(messages, list) else [messages]
            )
        )

def touch_user(user_id):
    now = datetime.now().isoformat()
    with db() as conn:
        conn.execute("""
        INSERT OR IGNORE INTO users (user_id, joined_date, last_active)
        VALUES (?, ?, ?)
        """, (user_id, now, now))
        conn.execute("""
        UPDATE users SET last_active=? WHERE user_id=?
        """, (now, user_id))

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
# الرسائل النصية
# --------------------------------------------------
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip().lower()
    touch_user(user_id)

    if text in ["بداية", "menu", "start", "القائمة"]:
        reply(event, FlexMessage(
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(create_main_menu())
        ))

    elif text.startswith("بحث:"):
        term = text.split(":", 1)[1]
        results = search_cards(term)
        if results:
            reply(event, FlexMessage(
                alt_text="نتائج البحث",
                contents=FlexContainer.from_dict(create_search_results(results, term))
            ))
        else:
            reply(event, TextMessage(text="❌ لا توجد نتائج"))

    else:
        reply(event, TextMessage(
            text="🌙 اكتب (بداية) لفتح القائمة\n🔍 بحث: اسم البطاقة"
        ))

# --------------------------------------------------
# Postback
# --------------------------------------------------
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data
    touch_user(user_id)

    if data == "action=reading_menu":
        reply(event, FlexMessage(
            alt_text="اختر قراءة",
            contents=FlexContainer.from_dict(create_reading_menu())
        ))

    elif data.startswith("action=reading&type="):
        rtype = data.split("=")[-1]
        result = perform_reading(user_id, rtype)

        reply(event, FlexMessage(
            alt_text=result["title"],
            contents=FlexContainer.from_dict(
                create_celtic_cross_result(result)
                if rtype == "celtic_cross"
                else create_spread_result(result)
            )
        ))

    elif data == "action=daily_card":
        card = get_daily_card(user_id)
        reply(event, FlexMessage(
            alt_text="بطاقة اليوم",
            contents=FlexContainer.from_dict(create_card_display(card, is_daily=True))
        ))

# --------------------------------------------------
# منطق التاروت
# --------------------------------------------------
def perform_reading(user_id, rtype):
    count = {
        "single": 1,
        "past_present_future": 3,
        "relationship": 3,
        "decision": 2,
        "celtic_cross": 10
    }.get(rtype, 1)

    cards = []
    for c in random.sample(TAROT_CARDS, count):
        card = c.copy()
        card["reversed"] = random.choice([True, False])
        cards.append(card)

    interpretation = get_tarot_interpretation(rtype, cards)

    with db() as conn:
        conn.execute(
            "INSERT INTO history (user_id, type, data, created_at) VALUES (?,?,?,?)",
            (user_id, rtype, str(cards), datetime.now().isoformat())
        )
        conn.execute(
            "UPDATE users SET readings = readings + 1 WHERE user_id=?",
            (user_id,)
        )

    return {
        "type": rtype,
        "cards": cards,
        "interpretation": interpretation,
        "title": "قراءة التاروت"
    }

def get_daily_card(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    with db() as conn:
        row = conn.execute(
            "SELECT card_id, reversed FROM daily WHERE user_id=? AND date=?",
            (user_id, today)
        ).fetchone()

        if row:
            card = get_card_by_id(row[0]).copy()
            card["reversed"] = bool(row[1])
            return card

        base = random.choice(TAROT_CARDS)
        card = base.copy()
        card["reversed"] = random.choice([True, False])

        conn.execute(
            "REPLACE INTO daily VALUES (?,?,?,?)",
            (user_id, card["id"], int(card["reversed"]), today)
        )
        return card

# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
