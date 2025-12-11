from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent
import os
import json
import random
from datetime import datetime
from tarot_data import TAROT_CARDS, get_tarot_interpretation
from flex_templates import (
    create_main_menu, create_reading_menu, create_card_display,
    create_spread_result, create_history_view
)

app = Flask(__name__)

# إعدادات Line Bot
CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_CHANNEL_ACCESS_TOKEN')

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# تخزين بسيط للبيانات (في الإنتاج استخدم قاعدة بيانات)
user_sessions = {}
reading_history = {}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        # القائمة الرئيسية
        if text in ['بداية', 'القائمة', 'menu', 'start']:
            flex_message = FlexMessage(
                alt_text="قائمة بوت التاروت",
                contents=FlexContainer.from_dict(create_main_menu())
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        # رسائل أخرى
        else:
            reply_text = "مرحباً بك في بوت التاروت\nاكتب 'بداية' لعرض القائمة الرئيسية"
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )

@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        # معالجة الأوامر المختلفة
        if data == 'action=reading_menu':
            flex_message = FlexMessage(
                alt_text="اختر نوع القراءة",
                contents=FlexContainer.from_dict(create_reading_menu())
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        elif data.startswith('action=reading&type='):
            reading_type = data.split('type=')[1]
            result = perform_reading(user_id, reading_type)
            
            flex_message = FlexMessage(
                alt_text=f"قراءة التاروت - {result['title']}",
                contents=FlexContainer.from_dict(create_spread_result(result))
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        elif data == 'action=daily_card':
            card = get_daily_card(user_id)
            flex_message = FlexMessage(
                alt_text=f"بطاقة اليوم - {card['name_ar']}",
                contents=FlexContainer.from_dict(create_card_display(card, is_daily=True))
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        elif data == 'action=history':
            history = get_user_history(user_id)
            flex_message = FlexMessage(
                alt_text="سجل القراءات السابقة",
                contents=FlexContainer.from_dict(create_history_view(history))
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        elif data == 'action=about':
            about_text = """
معلومات عن بوت التاروت

هذا البوت يقدم قراءات تاروت احترافية ومجانية باستخدام مجموعة كاملة من 78 بطاقة تاروت.

أنواع القراءات المتاحة:
- قراءة بطاقة واحدة: للأسئلة السريعة
- قراءة الماضي والحاضر والمستقبل: قراءة شاملة
- قراءة العلاقات: لفهم العلاقات العاطفية
- قراءة القرار: للمساعدة في اتخاذ القرارات
- البطاقة اليومية: نصيحة يومية

ملاحظة: قراءات التاروت للترفيه والإرشاد فقط
"""
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=about_text)]
                )
            )
        
        elif data == 'action=main_menu':
            flex_message = FlexMessage(
                alt_text="القائمة الرئيسية",
                contents=FlexContainer.from_dict(create_main_menu())
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )

def perform_reading(user_id, reading_type):
    """تنفيذ قراءة التاروت"""
    cards_needed = {
        'single': 1,
        'past_present_future': 3,
        'relationship': 3,
        'decision': 2
    }
    
    num_cards = cards_needed.get(reading_type, 1)
    selected_cards = random.sample(TAROT_CARDS, num_cards)
    
    # إضافة اتجاه عشوائي لكل بطاقة
    for card in selected_cards:
        card['reversed'] = random.choice([True, False])
    
    result = {
        'type': reading_type,
        'cards': selected_cards,
        'timestamp': datetime.now().isoformat(),
        'interpretation': get_tarot_interpretation(reading_type, selected_cards)
    }
    
    # حفظ في السجل
    if user_id not in reading_history:
        reading_history[user_id] = []
    reading_history[user_id].insert(0, result)
    
    # الاحتفاظ بآخر 10 قراءات فقط
    if len(reading_history[user_id]) > 10:
        reading_history[user_id] = reading_history[user_id][:10]
    
    # إضافة عنوان القراءة
    titles = {
        'single': 'قراءة بطاقة واحدة',
        'past_present_future': 'الماضي والحاضر والمستقبل',
        'relationship': 'قراءة العلاقات',
        'decision': 'قراءة القرار'
    }
    result['title'] = titles.get(reading_type, 'قراءة التاروت')
    
    return result

def get_daily_card(user_id):
    """الحصول على بطاقة اليوم"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # التحقق إذا كان المستخدم حصل على بطاقة اليوم
    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    
    if user_sessions[user_id].get('daily_date') != today:
        # بطاقة جديدة لهذا اليوم
        card = random.choice(TAROT_CARDS).copy()
        card['reversed'] = random.choice([True, False])
        user_sessions[user_id]['daily_card'] = card
        user_sessions[user_id]['daily_date'] = today
    
    return user_sessions[user_id]['daily_card']

def get_user_history(user_id):
    """الحصول على سجل قراءات المستخدم"""
    return reading_history.get(user_id, [])

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
