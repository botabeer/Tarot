from datetime import datetime

# --------------------------------------------------
# ألوان احترافية ومريحة للعين
# --------------------------------------------------
COLORS = {
    "primary": "#5E35B1",
    "secondary": "#7E57C2",
    "accent": "#FF4081",
    "bg": "#F5F5F5",
    "text": "#212121",
    "muted": "#757575",
    "white": "#FFFFFF",
    "shadow": "#D1C4E9",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336"
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
        "backgroundColor": COLORS["primary"],
        "cornerRadius": "md"
    }


def create_button(label, data, style="primary"):
    btn = {
        "type": "button",
        "action": {"type": "postback", "label": label, "data": data},
        "height": "sm",
        "margin": "sm"
    }
    if style == "primary":
        btn["style"] = "primary"
        btn["color"] = COLORS["primary"]
    elif style == "link":
        btn["style"] = "link"
        btn["color"] = COLORS["muted"]
    elif style == "secondary":
        btn["style"] = "secondary"
    return btn


def create_separator():
    return {"type": "separator", "margin": "md", "color": COLORS["shadow"]}


def create_stat_row(label, value):
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {"type": "text", "text": label, "size": "sm", "color": COLORS["text"], "flex": 0},
            {"type": "text", "text": str(value), "size": "sm", "color": COLORS["primary"], "align": "end", "weight": "bold"}
        ],
        "margin": "md"
    }


def format_time(ts):
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return ts


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
                {"type": "text", "text": "🌙 بوت التاروت الشامل", "size": "xl", "weight": "bold", "align": "center", "color": COLORS["white"]},
                {"type": "text", "text": "اختر ما يناسبك", "size": "sm", "align": "center", "color": COLORS["accent"], "margin": "md"}
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
                {"type": "text", "text": "✨ مرحباً بك في عالم التاروت", "size": "xs", "color": COLORS["muted"], "align": "center"}
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
                create_button("✨ الصليب السلتي (10)", "action=reading&type=celtic_cross"),
                create_separator(),
                create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")
            ],
            "paddingAll": "20px"
        }
    }


# --------------------------------------------------
# عرض بطاقة واحدة
# --------------------------------------------------
def create_card_display(card, is_daily=False, is_learning=False):
    direction = "معكوسة 🔄" if card.get("reversed") else "مستقيمة ⬆️"
    meaning = card["meaning_reversed"] if card.get("reversed") else card["meaning_upright"]
    title = "🔮 بطاقة اليوم" if is_daily else f"🎴 {card['name_ar']}"
    keywords_text = " • ".join(card.get("keywords", [])[:3])
    
    return {
        "type": "bubble",
        "header": create_header(title),
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": card["name"], "size": "lg", "weight": "bold", "align": "center", "color": COLORS["white"]},
                {"type": "text", "text": direction, "size": "sm", "align": "center", "color": COLORS["accent"], "margin": "sm"}
            ],
            "paddingAll": "20px",
            "backgroundColor": card.get("color", COLORS["secondary"])
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "✨ المعنى", "size": "sm", "weight": "bold", "color": COLORS["primary"]},
                {"type": "text", "text": meaning, "size": "sm", "color": COLORS["text"], "wrap": True, "margin": "md"},
                create_separator(),
                {"type": "text", "text": "🔑 الكلمات المفتاحية", "size": "xs", "weight": "bold", "color": COLORS["primary"], "margin": "md"},
                {"type": "text", "text": keywords_text, "size": "xs", "color": COLORS["secondary"], "wrap": True, "margin": "sm"}
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")],
            "paddingAll": "10px"
        }
    }


# --------------------------------------------------
# نتائج القراءات
# --------------------------------------------------
def create_spread_result(result):
    bubbles = [create_card_display(card) for card in result["cards"]]
    
    bubbles.append({
        "type": "bubble",
        "header": create_header("✨ التفسير الشامل"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": result.get("interpretation", ""), "size": "sm", "color": COLORS["text"], "wrap": True},
                create_separator(),
                {"type": "text", "text": f"📅 {format_time(result.get('timestamp', ''))}", "size": "xs", "color": COLORS["muted"], "align": "center", "margin": "md"}
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_button("🔄 قراءة جديدة", "action=reading_menu"),
                create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")
            ],
            "paddingAll": "10px"
        }
    })
    
    return {"type": "carousel", "contents": bubbles}


# --------------------------------------------------
# الصليب السلتي
# --------------------------------------------------
def create_celtic_cross_result(result):
    positions = [
        "1️⃣ الوضع الحالي", "2️⃣ التحدي", "3️⃣ السبب الجذري", "4️⃣ الماضي",
        "5️⃣ الإمكانات", "6️⃣ المستقبل القريب", "7️⃣ أنت", "8️⃣ الآخرون",
        "9️⃣ الآمال والمخاوف", "🔟 النتيجة"
    ]
    
    bubbles = []
    for i, card in enumerate(result["cards"][:10]):
        direction = "معكوسة" if card["reversed"] else "مستقيمة"
        meaning = card["meaning_reversed"] if card["reversed"] else card["meaning_upright"]
        
        if len(meaning) > 180:
            meaning = meaning[:177] + "..."
        
        bubbles.append({
            "type": "bubble",
            "header": create_header(positions[i]),
            "hero": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": card["name_ar"], "size": "lg", "weight": "bold", "align": "center", "color": COLORS["white"]},
                    {"type": "text", "text": f"{card['name']} • {direction}", "size": "xs", "align": "center", "color": COLORS["accent"], "margin": "sm"}
                ],
                "paddingAll": "15px",
                "backgroundColor": card.get("color", COLORS["secondary"])
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": meaning, "size": "sm", "color": COLORS["text"], "wrap": True}
                ],
                "paddingAll": "15px"
            }
        })
    
    # إضافة الملخص النهائي
    bubbles.append({
        "type": "bubble",
        "header": create_header("✨ الملخص النهائي"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": result.get("interpretation", "تحليل شامل للقراءة"), "size": "sm", "color": COLORS["text"], "wrap": True}
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")],
            "paddingAll": "10px"
        }
    })
    
    return {"type": "carousel", "contents": bubbles}


# --------------------------------------------------
# الإحصائيات
# --------------------------------------------------
def create_stats_view(stats):
    xp = stats.get("xp", 0)
    level = stats.get("level", 1)
    title = stats.get("title", "مبتدئ 🌱")
    next_level_xp = stats.get("next_level_xp", 100)
    
    return {
        "type": "bubble",
        "header": create_header("📊 إحصائياتك"),
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": title, "size": "xl", "weight": "bold", "align": "center", "color": COLORS["white"]},
                {"type": "text", "text": f"المستوى {level}", "size": "md", "align": "center", "color": COLORS["accent"], "margin": "md"},
                {"type": "text", "text": f"نقاط الخبرة: {xp} / {next_level_xp}", "size": "sm", "align": "center", "color": COLORS["white"], "margin": "sm"}
            ],
            "paddingAll": "20px",
            "backgroundColor": COLORS["primary"]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_stat_row("📖 القراءات", stats.get("readings_count", 0)),
                create_stat_row("🎴 البطاقات المشاهدة", len(stats.get("cards_viewed", []))),
                create_stat_row("🔮 بطاقات اليوم", stats.get("daily_cards_count", 0)),
                create_stat_row("📚 الدروس المكتملة", len(stats.get("lessons_completed", []))),
                create_stat_row("🎯 الاختبارات المنجزة", len(stats.get("quizzes_passed", []))),
                create_separator(),
                {"type": "text", "text": "استمر في رحلتك الروحية! ✨", "size": "xs", "color": COLORS["secondary"], "align": "center", "margin": "md"}
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")],
            "paddingAll": "10px"
        }
    }


# --------------------------------------------------
# نتائج البحث
# --------------------------------------------------
def create_search_results(results, term):
    bubbles = [create_card_display({**card, "reversed": False}, is_learning=True) for card in results[:10]]
    return {"type": "carousel", "contents": bubbles}


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
                {"type": "text", "text": "تعلم المزيد عن التاروت", "size": "sm", "color": COLORS["muted"], "wrap": True},
                create_separator(),
                create_button("🌱 دليل المبتدئين", "action=beginner_guide"),
                create_button("📖 الدروس التعليمية", "action=lessons_list"),
                create_button("🎴 مكتبة البطاقات", "action=card_library"),
                create_button("💪 التمرين اليومي", "action=daily_practice"),
                create_button("🌟 تقدمك التعليمي", "action=progress"),
                create_separator(),
                create_button("↩️ القائمة الرئيسية", "action=main_menu", style="link")
            ],
            "paddingAll": "20px"
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
                {"type": "text", "text": "📖 ما هو التاروت؟", "size": "md", "weight": "bold", "color": COLORS["primary"]},
                {"type": "text", "text": "التاروت أداة للتأمل الذاتي والاستبصار، وليس للتنبؤ الحتمي بالمستقبل.", "size": "sm", "color": COLORS["text"], "wrap": True, "margin": "md"},
                create_separator(),
                {"type": "text", "text": "🎴 البطاقات", "size": "md", "weight": "bold", "color": COLORS["primary"], "margin": "md"},
                {"type": "text", "text": "• 78 بطاقة: 22 بطاقة كبرى + 56 بطاقة صغرى\n• كل بطاقة تحمل معنى نفسي وروحي\n• البطاقات المعكوسة تعني طاقة داخلية أو تأخير", "size": "sm", "color": COLORS["text"], "wrap": True, "margin": "md"},
                create_separator(),
                {"type": "text", "text": "💡 نصيحة", "size": "md", "weight": "bold", "color": COLORS["primary"], "margin": "md"},
                {"type": "text", "text": "استخدم القراءات للتفكير في حياتك واتخاذ قرارات واعية. الأمر يتعلق بالحكمة الداخلية.", "size": "sm", "color": COLORS["text"], "wrap": True, "margin": "md"}
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [create_button("↩️ مركز التعلم", "action=learning_menu", style="link")],
            "paddingAll": "10px"
        }
    }


def create_lessons_list(progress):
    from tarot_data import LESSONS
    
    lessons_completed = progress.get("lessons_completed", [])
    
    contents = []
    for lesson in LESSONS:
        status = "✅" if lesson["id"] in lessons_completed else "📖"
        btn = create_button(f"{status} {lesson['title']}", f"action=lesson&id={lesson['id']}")
        contents.append(btn)
    
    contents.append(create_separator())
    contents.append(create_button("↩️ مركز التعلم", "action=learning_menu", style="link"))
    
    return {
        "type": "bubble",
        "header": create_header("📖 الدروس التعليمية"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": contents,
            "paddingAll": "20px"
        }
    }


def create_lesson_detail(lesson, progress):
    lessons_completed = progress.get("lessons_completed", [])
    is_completed = lesson["id"] in lessons_completed
    
    return {
        "type": "bubble",
        "header": create_header(f"📖 {lesson['title']}"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": lesson["content"], "size": "sm", "color": COLORS["text"], "wrap": True},
                create_separator(),
                {"type": "text", "text": "✅ درس مكتمل!" if is_completed else "📝 درس جديد", "size": "xs", "color": COLORS["success"] if is_completed else COLORS["primary"], "align": "center", "margin": "md"}
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [create_button("↩️ قائمة الدروس", "action=lessons_list", style="link")],
            "paddingAll": "10px"
        }
    }


def create_card_library(progress):
    from tarot_data import TAROT_CARDS
    
    cards_viewed = progress.get("cards_viewed", [])
    major_cards = [c for c in TAROT_CARDS if c["suit"] == "major"][:10]
    
    contents = [
        {"type": "text", "text": f"🎴 البطاقات المشاهدة: {len(cards_viewed)}/78", "size": "sm", "color": COLORS["muted"], "align": "center"},
        create_separator()
    ]
    
    for card in major_cards:
        status = "✅" if card["id"] in cards_viewed else "🎴"
        btn = create_button(f"{status} {card['name_ar']}", f"action=card_detail&id={card['id']}")
        contents.append(btn)
    
    contents.append(create_separator())
    contents.append({"type": "text", "text": "المزيد من البطاقات قريباً...", "size": "xs", "color": COLORS["muted"], "align": "center", "margin": "md"})
    contents.append(create_button("↩️ مركز التعلم", "action=learning_menu", style="link"))
    
    return {
        "type": "bubble",
        "header": create_header("🎴 مكتبة البطاقات"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": contents,
            "paddingAll": "20px"
        }
    }


def create_quiz(quiz, question_index):
    question = quiz["questions"][question_index]
    
    options_buttons = []
    for i, option in enumerate(question["options"]):
        btn = create_button(option, f"action=answer&quiz={quiz['id']}&q={question_index}&a={i}")
        options_buttons.append(btn)
    
    return {
        "type": "bubble",
        "header": create_header(f"🎯 {quiz['title']}"),
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"السؤال {question_index + 1}/{len(quiz['questions'])}", "size": "xs", "color": COLORS["muted"], "align": "center"},
                create_separator(),
                {"type": "text", "text": question["question"], "size": "md", "color": COLORS["text"], "wrap": True, "margin": "md", "weight": "bold"},
                create_separator()
            ] + options_buttons,
            "paddingAll": "20px"
        }
    }


def create_quiz_result(quiz, score, total, passed):
    percentage = int((score / total) * 100)
    emoji = "🎉" if passed else "💪"
    status = "نجحت!" if passed else "حاول مرة أخرى"
    color = COLORS["success"] if passed else COLORS["warning"]
    
    return {
        "type": "bubble",
        "header": create_header(f"{emoji} نتيجة الاختبار"),
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": status, "size": "xl", "weight": "bold", "align": "center", "color": COLORS["white"]},
                {"type": "text", "text": f"{score} من {total}", "size": "lg", "align": "center", "color": COLORS["accent"], "margin": "md"},
                {"type": "text", "text": f"{percentage}%", "size": "md", "align": "center", "color": COLORS["white"], "margin": "sm"}
            ],
            "paddingAll": "20px",
            "backgroundColor": color
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "تحتاج 70% للنجاح" if not passed else "أحسنت! 🌟", "size": "sm", "color": COLORS["text"], "align": "center", "wrap": True}
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_button("🔄 إعادة المحاولة", f"action=quiz&id={quiz['id']}") if not passed else create_button("✨ اختبار آخر", "action=learning_menu"),
                create_button("↩️ مركز التعلم", "action=learning_menu", style="link")
            ],
            "paddingAll": "10px"
        }
    }


def create_progress_view(progress):
    lessons_count = len(progress.get("lessons_completed", []))
    quizzes_count = len(progress.get("quizzes_passed", []))
    cards_count = len(progress.get("cards_viewed", []))
    xp = progress.get("xp", 0)
    level = progress.get("level", 1)
    
    return {
        "type": "bubble",
        "header": create_header("🌟 تقدمك التعليمي"),
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"المستوى {level}", "size": "xl", "weight": "bold", "align": "center", "color": COLORS["white"]},
                {"type": "text", "text": f"نقاط الخبرة: {xp}", "size": "md", "align": "center", "color": COLORS["accent"], "margin": "md"}
            ],
            "paddingAll": "20px",
            "backgroundColor": COLORS["primary"]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_stat_row("📖 الدروس المكتملة", f"{lessons_count}/5"),
                create_stat_row("🎯 الاختبارات المنجزة", f"{quizzes_count}/3"),
                create_stat_row("🎴 البطاقات المشاهدة", f"{cards_count}/78"),
                create_separator(),
                {"type": "text", "text": "استمر في التعلم لفتح محتوى جديد! 🚀", "size": "xs", "color": COLORS["secondary"], "align": "center", "margin": "md", "wrap": True}
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [create_button("↩️ مركز التعلم", "action=learning_menu", style="link")],
            "paddingAll": "10px"
        }
    }


def create_daily_practice(practice):
    return {
        "type": "bubble",
        "header": create_header("💪 التمرين اليومي"),
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": practice["card"]["name_ar"], "size": "lg", "weight": "bold", "align": "center", "color": COLORS["white"]},
                {"type": "text", "text": practice["card"]["name"], "size": "sm", "align": "center", "color": COLORS["accent"], "margin": "sm"}
            ],
            "paddingAll": "15px",
            "backgroundColor": practice["card"].get("color", COLORS["secondary"])
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "❓ السؤال", "size": "sm", "weight": "bold", "color": COLORS["primary"]},
                {"type": "text", "text": practice["question"], "size": "sm", "color": COLORS["text"], "wrap": True, "margin": "md"},
                create_separator(),
                {"type": "text", "text": "💡 الإجابة", "size": "sm", "weight": "bold", "color": COLORS["primary"], "margin": "md"},
                {"type": "text", "text": practice["answer"], "size": "sm", "color": COLORS["text"], "wrap": True, "margin": "md"},
                create_separator(),
                {"type": "text", "text": f"🎁 مكافأة: +{practice['xp_reward']} نقطة خبرة", "size": "xs", "color": COLORS["success"], "align": "center", "margin": "md"}
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [create_button("↩️ مركز التعلم", "action=learning_menu", style="link")],
            "paddingAll": "10px"
        }
    }
