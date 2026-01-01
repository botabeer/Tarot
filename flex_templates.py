from datetime import datetime

# --------------------------------------------------
# ألوان موحدة
# --------------------------------------------------
COLORS = {
    "primary": "#6A0DAD",
    "secondary": "#9370DB",
    "accent": "#FF6B9D",
    "bg": "#F8F8F8",
    "text": "#333333",
    "muted": "#777777",
    "white": "#FFFFFF"
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
                    "color": COLORS["white"]
                },
                {
                    "type": "text",
                    "text": "اختر ما يناسبك",
                    "size": "sm",
                    "align": "center",
                    "color": "#E6E6FA",
                    "margin": "md"
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
                create_button("🎴 قراءات التاروت", "action=reading_menu"),
                create_button("🔮 بطاقة اليوم", "action=daily_card"),
                create_button("📚 التعلم", "action=learning_menu"),
                create_button("📊 إحصائياتي", "action=stats")
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "✨ مرحباً بك في عالم التاروت",
                    "size": "xs",
                    "color": COLORS["muted"],
                    "align": "center"
                }
            ],
            "paddingAll": "10px"
        }
    }

# --------------------------------------------------
# قائمة القراءات
# --------------------------------------------------
def create_reading_menu():
    return {
        "type": "bubble",
        "header": create_header("🎴 اختر نوع القراءة"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                create_button("🎯 بطاقة واحدة", "action=reading&type=single"),
                create_button("⏳ الماضي والحاضر والمستقبل", "action=reading&type=past_present_future"),
                create_button("💕 العلاقات", "action=reading&type=relationship"),
                create_button("🤔 اتخاذ قرار", "action=reading&type=decision"),
                create_button("✨ الصليب السلتي (10)", "action=reading&type=celtic_cross")
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")
            ],
            "paddingAll": "10px"
        }
    }

# --------------------------------------------------
# عرض بطاقة واحدة
# --------------------------------------------------
def create_card_display(card, is_daily=False, is_learning=False):
    direction = "معكوسة 🔄" if card.get("reversed") else "مستقيمة ⬆️"
    meaning = card["meaning_reversed"] if card.get("reversed") else card["meaning_upright"]
    
    title = "🔮 بطاقة اليوم" if is_daily else card["name_ar"]
    
    keywords_text = " • ".join(card.get("keywords", [])[:3])
    
    return {
        "type": "bubble",
        "header": create_header(title),
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": card["name"],
                    "size": "lg",
                    "weight": "bold",
                    "align": "center",
                    "color": COLORS["white"]
                },
                {
                    "type": "text",
                    "text": direction,
                    "size": "sm",
                    "align": "center",
                    "color": "#E6E6FA",
                    "margin": "sm"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": card.get("color", COLORS["secondary"])
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "✨ المعنى",
                    "size": "sm",
                    "weight": "bold",
                    "color": COLORS["primary"],
                    "margin": "none"
                },
                {
                    "type": "text",
                    "text": meaning,
                    "size": "sm",
                    "color": COLORS["text"],
                    "wrap": True,
                    "margin": "md"
                },
                create_separator(),
                {
                    "type": "text",
                    "text": "🔑 الكلمات المفتاحية",
                    "size": "xs",
                    "weight": "bold",
                    "color": COLORS["primary"],
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": keywords_text,
                    "size": "xs",
                    "color": COLORS["secondary"],
                    "wrap": True,
                    "margin": "sm"
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")
            ],
            "paddingAll": "10px"
        }
    }

# --------------------------------------------------
# نتيجة قراءة عادية
# --------------------------------------------------
def create_spread_result(result):
    bubbles = []
    
    # إضافة البطاقات
    for idx, card in enumerate(result["cards"]):
        bubble = create_card_display(card)
        bubbles.append(bubble)
    
    # إضافة ملخص التفسير
    summary_bubble = {
        "type": "bubble",
        "header": create_header("✨ التفسير الشامل"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": result["interpretation"],
                    "size": "sm",
                    "color": COLORS["text"],
                    "wrap": True
                },
                create_separator(),
                {
                    "type": "text",
                    "text": f"📅 {format_time(result['timestamp'])}",
                    "size": "xs",
                    "color": COLORS["muted"],
                    "align": "center"
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_button("🔄 قراءة جديدة", "action=reading_menu", style="primary"),
                create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")
            ],
            "paddingAll": "10px",
            "spacing": "sm"
        }
    }
    
    bubbles.append(summary_bubble)
    
    return {
        "type": "carousel",
        "contents": bubbles
    }

# --------------------------------------------------
# الصليب السلتي (10 بطاقات)
# --------------------------------------------------
def create_celtic_cross_result(result):
    positions = [
        "1️⃣ الوضع الحالي",
        "2️⃣ التحدي",
        "3️⃣ السبب الجذري",
        "4️⃣ الماضي",
        "5️⃣ الإمكانات",
        "6️⃣ المستقبل القريب",
        "7️⃣ أنت",
        "8️⃣ الآخرون",
        "9️⃣ الآمال والمخاوف",
        "🔟 النتيجة"
    ]
    
    bubbles = []
    
    for i, card in enumerate(result["cards"][:10]):
        direction = "معكوسة" if card["reversed"] else "مستقيمة"
        meaning = card["meaning_reversed"] if card["reversed"] else card["meaning_upright"]
        
        # تقصير المعنى إذا كان طويلاً
        if len(meaning) > 180:
            meaning = meaning[:177] + "..."
        
        bubble = {
            "type": "bubble",
            "header": create_header(positions[i]),
            "hero": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": card["name_ar"],
                        "size": "lg",
                        "weight": "bold",
                        "align": "center",
                        "color": COLORS["white"]
                    },
                    {
                        "type": "text",
                        "text": f"{card['name']} • {direction}",
                        "size": "xs",
                        "align": "center",
                        "color": "#E6E6FA",
                        "margin": "sm"
                    }
                ],
                "paddingAll": "15px",
                "backgroundColor": card.get("color", COLORS["secondary"])
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": meaning,
                        "size": "sm",
                        "color": COLORS["text"],
                        "wrap": True
                    }
                ],
                "paddingAll": "15px"
            }
        }
        
        bubbles.append(bubble)
    
    # إضافة ملخص نهائي
    summary_bubble = {
        "type": "bubble",
        "header": create_header("✨ الملخص النهائي"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": result.get("interpretation", "تحليل شامل للقراءة"),
                    "size": "sm",
                    "color": COLORS["text"],
                    "wrap": True
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")
            ],
            "paddingAll": "10px"
        }
    }
    
    bubbles.append(summary_bubble)
    
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
        "header": create_header("📚 مركز التعلم"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "تعلم المزيد عن التاروت",
                    "size": "sm",
                    "color": COLORS["muted"],
                    "wrap": True
                },
                create_separator(),
                create_button("🌱 دليل المبتدئين", "action=beginner_guide"),
                {
                    "type": "text",
                    "text": "قريباً: معرض البطاقات الكامل",
                    "size": "xs",
                    "color": COLORS["muted"],
                    "align": "center",
                    "margin": "md"
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")
            ],
            "paddingAll": "10px"
        }
    }

def create_beginner_guide():
    return {
        "type": "bubble",
        "header": create_header("🌱 دليل المبتدئين"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "📖 ما هو التاروت؟",
                    "size": "md",
                    "weight": "bold",
                    "color": COLORS["primary"]
                },
                {
                    "type": "text",
                    "text": "التاروت أداة للتأمل الذاتي والاستبصار، وليس للتنبؤ الحتمي بالمستقبل.",
                    "size": "sm",
                    "color": COLORS["text"],
                    "wrap": True,
                    "margin": "md"
                },
                create_separator(),
                {
                    "type": "text",
                    "text": "🎴 البطاقات",
                    "size": "md",
                    "weight": "bold",
                    "color": COLORS["primary"],
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "• 78 بطاقة: 22 بطاقة كبرى + 56 بطاقة صغرى\n• كل بطاقة تحمل معنى نفسي وروحي\n• البطاقات المعكوسة تعني طاقة داخلية أو تأخير",
                    "size": "sm",
                    "color": COLORS["text"],
                    "wrap": True,
                    "margin": "md"
                },
                create_separator(),
                {
                    "type": "text",
                    "text": "💡 نصيحة",
                    "size": "md",
                    "weight": "bold",
                    "color": COLORS["primary"],
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "استخدم القراءات للتفكير في حياتك واتخاذ قرارات واعية. الأمر يتعلق بالحكمة الداخلية.",
                    "size": "sm",
                    "color": COLORS["text"],
                    "wrap": True,
                    "margin": "md"
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")
            ],
            "paddingAll": "10px"
        }
    }

# --------------------------------------------------
# الإحصائيات
# --------------------------------------------------
def create_stats_view(stats):
    total = stats.get("total", 0)
    level = stats.get("level", "مبتدئ 🌱")
    
    return {
        "type": "bubble",
        "header": create_header("📊 إحصائياتك"),
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": level,
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": COLORS["white"]
                },
                {
                    "type": "text",
                    "text": f"إجمالي النشاط: {total}",
                    "size": "sm",
                    "align": "center",
                    "color": "#E6E6FA",
                    "margin": "md"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": COLORS["primary"]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_stat_row("📖 القراءات", stats.get("readings_count", 0)),
                create_stat_row("🎴 البطاقات المشاهدة", stats.get("cards_viewed", 0)),
                create_stat_row("🔮 بطاقات اليوم", stats.get("daily_cards_count", 0)),
                create_separator(),
                {
                    "type": "text",
                    "text": "استمر في رحلتك الروحية! ✨",
                    "size": "xs",
                    "color": COLORS["secondary"],
                    "align": "center",
                    "margin": "md"
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")
            ],
            "paddingAll": "10px"
        }
    }

# --------------------------------------------------
# نتائج البحث
# --------------------------------------------------
def create_search_results(results, term):
    bubbles = []
    
    for card in results[:10]:
        card_copy = card.copy()
        card_copy["reversed"] = False
        bubble = create_card_display(card_copy, is_learning=True)
        bubbles.append(bubble)
    
    return {
        "type": "carousel",
        "contents": bubbles
    }

# --------------------------------------------------
# أدوات مساعدة
# --------------------------------------------------
def create_header(text_value):
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
                "color": COLORS["white"]
            }
        ],
        "paddingAll": "15px",
        "backgroundColor": COLORS["primary"]
    }

def create_button(label, data, style="primary"):
    button_config = {
        "type": "button",
        "action": {
            "type": "postback",
            "label": label,
            "data": data
        },
        "height": "sm"
    }
    
    if style == "primary":
        button_config["style"] = "primary"
        button_config["color"] = COLORS["primary"]
    elif style == "link":
        button_config["style"] = "link"
        button_config["color"] = COLORS["muted"]
    
    return button_config

def create_separator():
    return {
        "type": "separator",
        "margin": "md"
    }

def create_stat_row(label, value):
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": label,
                "size": "sm",
                "color": COLORS["text"],
                "flex": 0
            },
            {
                "type": "text",
                "text": str(value),
                "size": "sm",
                "color": COLORS["primary"],
                "align": "end",
                "weight": "bold"
            }
        ],
        "margin": "md"
    }

def format_time(ts):
    """تنسيق الوقت"""
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return ts
