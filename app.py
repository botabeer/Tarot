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
from datetime import datetime, timedelta
from tarot_data import TAROT_CARDS, get_tarot_interpretation, get_card_by_id
from flex_templates import (
    create_main_menu, create_reading_menu, create_card_display,
    create_spread_result, create_history_view, create_learning_menu,
    create_card_gallery, create_beginner_guide, create_celtic_cross_result,
    create_stats_view, create_daily_tips, create_search_results
)

app = Flask(__name__)

# إعدادات Line Bot
CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_CHANNEL_ACCESS_TOKEN')

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# تخزين البيانات (في الإنتاج استخدم قاعدة بيانات)
user_sessions = {}
reading_history = {}
user_progress = {}  # لتتبع تقدم التعلم
user_favorites = {}  # البطاقات المفضلة

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
        if text in ['بداية', 'القائمة', 'menu', 'start', 'البداية']:
            initialize_user(user_id)
            flex_message = FlexMessage(
                alt_text="قائمة بوت التاروت الشامل",
                contents=FlexContainer.from_dict(create_main_menu())
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        # البحث عن بطاقة
        elif text.startswith('بحث:') or text.startswith('search:'):
            search_term = text.split(':', 1)[1].strip()
            results = search_cards(search_term)
            if results:
                flex_message = FlexMessage(
                    alt_text=f"نتائج البحث: {search_term}",
                    contents=FlexContainer.from_dict(create_search_results(results, search_term))
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex_message]
                    )
                )
            else:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=f"لم أجد نتائج لـ '{search_term}'\nجرب البحث باسم البطاقة أو كلمة مفتاحية")]
                    )
                )
        
        # رسائل ترحيبية للمبتدئين
        elif any(word in text.lower() for word in ['مبتدئ', 'تعلم', 'شرح', 'كيف', 'ماذا', 'beginner', 'learn']):
            flex_message = FlexMessage(
                alt_text="دليل المبتدئين في التاروت",
                contents=FlexContainer.from_dict(create_beginner_guide())
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        # رسائل أخرى
        else:
            reply_text = """🌙 مرحباً بك في بوت التاروت الشامل

اكتب 'بداية' للقائمة الرئيسية

📚 للمبتدئين:
• اكتب 'تعلم' أو 'مبتدئ' لدليل شامل
• اكتب 'بحث: اسم البطاقة' للبحث

✨ أو اختر من القائمة:
• قراءات تاروت متنوعة
• معرض البطاقات الكامل
• دروس ونصائح يومية
• سجل قراءاتك وإحصائياتك"""
            
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
        
        # القائمة الرئيسية
        if data == 'action=main_menu':
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
        
        # قائمة القراءات
        elif data == 'action=reading_menu':
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
        
        # تنفيذ القراءات
        elif data.startswith('action=reading&type='):
            reading_type = data.split('type=')[1]
            result = perform_reading(user_id, reading_type)
            
            # استخدام تصميم خاص للصليب السلتي
            if reading_type == 'celtic_cross':
                flex_message = FlexMessage(
                    alt_text=f"قراءة التاروت - {result['title']}",
                    contents=FlexContainer.from_dict(create_celtic_cross_result(result))
                )
            else:
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
            
            # تحديث إحصائيات المستخدم
            update_user_stats(user_id, 'reading')
        
        # البطاقة اليومية
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
            update_user_stats(user_id, 'daily_card')
        
        # سجل القراءات
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
        
        # قائمة التعلم
        elif data == 'action=learning_menu':
            flex_message = FlexMessage(
                alt_text="مركز التعلم",
                contents=FlexContainer.from_dict(create_learning_menu())
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        # دليل المبتدئين
        elif data == 'action=beginner_guide':
            flex_message = FlexMessage(
                alt_text="دليل المبتدئين الشامل",
                contents=FlexContainer.from_dict(create_beginner_guide())
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        # معرض البطاقات
        elif data.startswith('action=card_gallery'):
            if '&suit=' in data:
                suit = data.split('suit=')[1]
                flex_message = FlexMessage(
                    alt_text=f"معرض البطاقات - {suit}",
                    contents=FlexContainer.from_dict(create_card_gallery(suit))
                )
            else:
                flex_message = FlexMessage(
                    alt_text="معرض البطاقات",
                    contents=FlexContainer.from_dict(create_card_gallery())
                )
            
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        # عرض بطاقة محددة
        elif data.startswith('action=view_card&id='):
            card_id = int(data.split('id=')[1])
            card = get_card_by_id(card_id)
            if card:
                # إضافة معلومات إضافية عن البطاقة
                card_copy = card.copy()
                card_copy['reversed'] = False  # عرض كلا الاتجاهين
                flex_message = FlexMessage(
                    alt_text=f"{card['name_ar']} - {card['name']}",
                    contents=FlexContainer.from_dict(create_card_display(card_copy, is_learning=True))
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex_message]
                    )
                )
                update_user_stats(user_id, 'card_viewed')
        
        # الإحصائيات
        elif data == 'action=stats':
            stats = get_user_stats(user_id)
            flex_message = FlexMessage(
                alt_text="إحصائياتك في التاروت",
                contents=FlexContainer.from_dict(create_stats_view(stats))
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        # نصائح يومية
        elif data == 'action=daily_tips':
            tips = get_daily_tips()
            flex_message = FlexMessage(
                alt_text="نصائح التاروت اليومية",
                contents=FlexContainer.from_dict(create_daily_tips(tips))
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )
        
        # حول البوت
        elif data == 'action=about':
            about_text = """🌙 بوت التاروت الشامل - دليلك الكامل

📚 ما يقدمه البوت:

🎴 قراءات متنوعة:
• بطاقة واحدة - للأسئلة السريعة
• الماضي والحاضر والمستقبل
• قراءة العلاقات - فهم عميق للعلاقات
• قراءة القرار - للاختيارات الصعبة
• الصليب السلتي - أشمل قراءة (10 بطاقات)

📖 مركز التعلم:
• دليل شامل للمبتدئين
• معرض 78 بطاقة كاملة
• شرح تفصيلي لكل بطاقة
• معاني البطاقات المستقيمة والمعكوسة

✨ ميزات إضافية:
• البطاقة اليومية
• نصائح يومية وأسبوعية
• سجل قراءاتك
• إحصائيات تقدمك
• بحث في البطاقات

⚠️ تنويه: قراءات التاروت للإرشاد والترفيه فقط
وليست بديلاً عن الاستشارة المهنية

💫 استمتع برحلتك في عالم التاروت!"""
            
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=about_text)]
                )
            )
        
        # إضافة/إزالة من المفضلة
        elif data.startswith('action=favorite&id='):
            card_id = int(data.split('id=')[1])
            toggle_favorite(user_id, card_id)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="تم تحديث المفضلة ✨")]
                )
            )

def initialize_user(user_id):
    """تهيئة بيانات المستخدم الجديد"""
    if user_id not in user_progress:
        user_progress[user_id] = {
            'readings_count': 0,
            'cards_viewed': 0,
            'daily_cards_count': 0,
            'favorite_cards': [],
            'joined_date': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat()
        }
    
    if user_id not in user_favorites:
        user_favorites[user_id] = []

def perform_reading(user_id, reading_type):
    """تنفيذ قراءة التاروت"""
    cards_needed = {
        'single': 1,
        'past_present_future': 3,
        'relationship': 3,
        'decision': 2,
        'celtic_cross': 10
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
    
    # الاحتفاظ بآخر 20 قراءة
    if len(reading_history[user_id]) > 20:
        reading_history[user_id] = reading_history[user_id][:20]
    
    # إضافة عنوان القراءة
    titles = {
        'single': 'قراءة بطاقة واحدة',
        'past_present_future': 'الماضي والحاضر والمستقبل',
        'relationship': 'قراءة العلاقات',
        'decision': 'قراءة القرار',
        'celtic_cross': 'الصليب السلتي'
    }
    result['title'] = titles.get(reading_type, 'قراءة التاروت')
    
    return result

def get_daily_card(user_id):
    """الحصول على بطاقة اليوم"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    
    if user_sessions[user_id].get('daily_date') != today:
        card = random.choice(TAROT_CARDS).copy()
        card['reversed'] = random.choice([True, False])
        user_sessions[user_id]['daily_card'] = card
        user_sessions[user_id]['daily_date'] = today
    
    return user_sessions[user_id]['daily_card']

def get_user_history(user_id):
    """الحصول على سجل قراءات المستخدم"""
    return reading_history.get(user_id, [])

def search_cards(search_term):
    """البحث في بطاقات التاروت"""
    search_term = search_term.lower()
    results = []
    
    for card in TAROT_CARDS:
        if (search_term in card['name'].lower() or 
            search_term in card['name_ar'].lower() or
            any(search_term in keyword.lower() for keyword in card['keywords'])):
            results.append(card)
    
    return results[:10]  # أول 10 نتائج

def update_user_stats(user_id, stat_type):
    """تحديث إحصائيات المستخدم"""
    if user_id not in user_progress:
        initialize_user(user_id)
    
    if stat_type == 'reading':
        user_progress[user_id]['readings_count'] += 1
    elif stat_type == 'card_viewed':
        user_progress[user_id]['cards_viewed'] += 1
    elif stat_type == 'daily_card':
        user_progress[user_id]['daily_cards_count'] += 1
    
    user_progress[user_id]['last_active'] = datetime.now().isoformat()

def get_user_stats(user_id):
    """الحصول على إحصائيات المستخدم"""
    if user_id not in user_progress:
        initialize_user(user_id)
    
    stats = user_progress[user_id].copy()
    
    # حساب مدة الاستخدام
    joined = datetime.fromisoformat(stats['joined_date'])
    days_active = (datetime.now() - joined).days
    stats['days_active'] = days_active
    
    # حساب مستوى الخبرة
    total_activity = (stats['readings_count'] + 
                     stats['cards_viewed'] + 
                     stats['daily_cards_count'])
    
    if total_activity < 10:
        stats['level'] = 'مبتدئ 🌱'
    elif total_activity < 50:
        stats['level'] = 'متعلم 📚'
    elif total_activity < 100:
        stats['level'] = 'متمرس ✨'
    else:
        stats['level'] = 'خبير 🌟'
    
    return stats

def get_daily_tips():
    """الحصول على نصائح يومية"""
    tips = [
        {
            'title': 'نصيحة اليوم',
            'content': 'التاروت أداة للتأمل الذاتي وليس للتنبؤ المطلق بالمستقبل'
        },
        {
            'title': 'تمرين اليوم',
            'content': 'اختر بطاقة عشوائية وتأمل في معناها لمدة 5 دقائق'
        },
        {
            'title': 'معلومة اليوم',
            'content': 'البطاقات المعكوسة ليست سلبية دائماً - قد تعني طاقة داخلية أو تأخيراً'
        }
    ]
    
    today_index = datetime.now().timetuple().tm_yday % len(tips)
    return tips[today_index]

def toggle_favorite(user_id, card_id):
    """إضافة/إزالة بطاقة من المفضلة"""
    if user_id not in user_favorites:
        user_favorites[user_id] = []
    
    if card_id in user_favorites[user_id]:
        user_favorites[user_id].remove(card_id)
    else:
        user_favorites[user_id].append(card_id)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
