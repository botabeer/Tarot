from datetime import datetime

# --------------------------------------------------
# ألوان موحدة
# --------------------------------------------------
COLORS = {
    "primary": "#6A0DAD",
    "secondary": "#9370DB",
    "bg": "#F8F8F8",
    "text": "#333333",
    "muted": "#777777"
}

# --------------------------------------------------
# القائمة الرئيسية
# --------------------------------------------------
def create_main_menu():
    return {
        "type": "bubble",
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🌙 بوت التاروت الشامل",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#FFFFFF"
                },
                {
                    "type": "text",
                    "text": "اختر ما يناسبك",
                    "size": "sm",
                    "align": "center",
                    "color": "#E6E6FA",
                    "margin": "sm"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": COLORS["primary"]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                button("🎴 قراءات التاروت", "action=reading_menu"),
                button("🔮 بطاقة اليوم", "action=daily_card"),
                button("📚 التعلم", "action=learning_menu"),
                button("📊 إحصائياتي", "action=stats")
            ]
        }
    }

# --------------------------------------------------
# قائمة القراءات
# --------------------------------------------------
def create_reading_menu():
    return {
        "type": "bubble",
        "header": header("🎴 اختر نوع القراءة"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                button("بطاقة واحدة", "action=reading&type=single"),
                button("الماضي / الحاضر / المستقبل", "action=reading&type=past_present_future"),
                button("العلاقات", "action=reading&type=relationship"),
                button("اتخاذ قرار", "action=reading&type=decision"),
                button("الصليب السلتي (10)", "action=reading&type=celtic_cross")
            ]
        }
    }

# --------------------------------------------------
# عرض بطاقة واحدة
# --------------------------------------------------
def create_card_display(card, is_daily=False, is_learning=False):
    direction = "معكوسة" if card.get("reversed") else "مستقيمة"
    meaning = card["meaning_reversed"] if card.get("reversed") else card["meaning_upright"]

    return {
        "type": "bubble",
        "header": header(card["name_ar"]),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                text(f"{card['name']} • {direction}", "sm", COLORS["muted"]),
                spacer(),
                text(meaning, "sm"),
                spacer(),
                text(" • ".join(card.get("keywords", [])), "xs", COLORS["secondary"])
            ]
        }
    }

# --------------------------------------------------
# نتيجة قراءة عادية
# --------------------------------------------------
def create_spread_result(result):
    bubbles = []

    for card in result["cards"]:
        bubbles.append(create_card_display(card))

    bubbles.append({
        "type": "bubble",
        "header": header("✨ الخلاصة"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                text(result["interpretation"], "sm"),
                spacer(),
                text(format_time(result["timestamp"]), "xs", COLORS["muted"])
            ]
        }
    })

    return {
        "type": "carousel",
        "contents": bubbles
    }

# --------------------------------------------------
# الصليب السلتي (10 بطاقات)
# --------------------------------------------------
def create_celtic_cross_result(result):
    positions = [
        "الوضع الحالي", "التحدي", "السبب الجذري", "الماضي",
        "الإمكانات", "المستقبل القريب", "أنت", "الآخرون",
        "الآمال والمخاوف", "النتيجة"
    ]

    bubbles = []

    for i, card in enumerate(result["cards"]):
        direction = "معكوسة" if card["reversed"] else "مستقيمة"
        meaning = card["meaning_reversed"] if card["reversed"] else card["meaning_upright"]

        bubbles.append({
            "type": "bubble",
            "header": header(f"{i+1}️⃣ {positions[i]}"),
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    text(f"{card['name_ar']} ({direction})", "sm", COLORS["secondary"]),
                    spacer(),
                    text(meaning[:180] + "..." if len(meaning) > 180 else meaning, "sm")
                ]
            }
        })

    return {
        "type": "carousel",
        "contents": bubbles
    }

# --------------------------------------------------
# مركز التعلم
# --------------------------------------------------
def create_learning_menu():
    return {
        "type": "bubble",
        "header": header("📚 مركز التعلم"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                button("دليل المبتدئين", "action=beginner_guide"),
                button("معرض البطاقات", "action=card_gallery")
            ]
        }
    }

def create_beginner_guide():
    return {
        "type": "bubble",
        "header": header("🌱 دليل المبتدئين"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                text("التاروت أداة للتأمل الذاتي وليس للتنبؤ الحتمي.", "sm"),
                spacer(),
                text("كل بطاقة تحمل معنى نفسي وروحي.", "sm"),
                spacer(),
                text("البطاقات المعكوسة تعني طاقة داخلية أو تأخير.", "sm")
            ]
        }
    }

# --------------------------------------------------
# الإحصائيات
# --------------------------------------------------
def create_stats_view(stats):
    return {
        "type": "bubble",
        "header": header("📊 إحصائياتك"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                text(f"📖 القراءات: {stats['readings_count']}", "sm"),
                text(f"🎴 البطاقات المشاهدة: {stats['cards_viewed']}", "sm"),
                text(f"🔮 بطاقات اليوم: {stats['daily_cards_count']}", "sm"),
                spacer(),
                text(f"⭐ المستوى: {stats['level']}", "md", COLORS["secondary"])
            ]
        }
    }

# --------------------------------------------------
# البحث
# --------------------------------------------------
def create_search_results(results, term):
    bubbles = []
    for card in results:
        bubbles.append(create_card_display(card))
    return {
        "type": "carousel",
        "contents": bubbles
    }

# --------------------------------------------------
# أدوات مساعدة
# --------------------------------------------------
def header(text_value):
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": text_value,
                "size": "lg",
                "weight": "bold",
                "align": "center",
                "color": "#FFFFFF"
            }
        ],
        "paddingAll": "15px",
        "backgroundColor": COLORS["primary"]
    }

def button(label, data):
    return {
        "type": "button",
        "style": "primary",
        "color": COLORS["primary"],
        "action": {
            "type": "postback",
            "label": label,
            "data": data
        }
    }

def text(value, size="sm", color=COLORS["text"]):
    return {
        "type": "text",
        "text": value,
        "size": size,
        "color": color,
        "wrap": True
    }

def spacer():
    return {
        "type": "spacer",
        "size": "md"
    }

def format_time(ts):
    return datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M")
