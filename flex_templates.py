from datetime import datetime

def create_main_menu():
    """القائمة الرئيسية"""
    return {
        "type": "bubble",
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "بوت التاروت",
                    "weight": "bold",
                    "size": "xxl",
                    "align": "center",
                    "color": "#8B4789"
                },
                {
                    "type": "text",
                    "text": "اكتشف ما تخبئه لك البطاقات",
                    "size": "sm",
                    "align": "center",
                    "color": "#999999",
                    "margin": "md"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#F5F5DC"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#8B4789",
                    "action": {
                        "type": "postback",
                        "label": "قراءة التاروت",
                        "data": "action=reading_menu"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#9370DB",
                    "action": {
                        "type": "postback",
                        "label": "البطاقة اليومية",
                        "data": "action=daily_card"
                    },
                    "margin": "md"
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "action": {
                        "type": "postback",
                        "label": "سجل القراءات",
                        "data": "action=history"
                    },
                    "margin": "md"
                },
                {
                    "type": "button",
                    "style": "link",
                    "action": {
                        "type": "postback",
                        "label": "عن البوت",
                        "data": "action=about"
                    },
                    "margin": "md"
                }
            ],
            "spacing": "md",
            "paddingAll": "20px"
        }
    }

def create_reading_menu():
    """قائمة أنواع القراءات"""
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "اختر نوع القراءة",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "color": "#FFFFFF"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#8B4789"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "قراءة بطاقة واحدة",
                            "weight": "bold",
                            "size": "md",
                            "color": "#8B4789"
                        },
                        {
                            "type": "text",
                            "text": "للأسئلة السريعة والمباشرة",
                            "size": "xs",
                            "color": "#999999",
                            "margin": "xs"
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#8B4789",
                            "action": {
                                "type": "postback",
                                "label": "ابدأ القراءة",
                                "data": "action=reading&type=single"
                            },
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#F0E6F6",
                    "paddingAll": "15px",
                    "cornerRadius": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "الماضي والحاضر والمستقبل",
                            "weight": "bold",
                            "size": "md",
                            "color": "#9370DB"
                        },
                        {
                            "type": "text",
                            "text": "قراءة شاملة لرحلتك",
                            "size": "xs",
                            "color": "#999999",
                            "margin": "xs"
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#9370DB",
                            "action": {
                                "type": "postback",
                                "label": "ابدأ القراءة",
                                "data": "action=reading&type=past_present_future"
                            },
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#E6E6FA",
                    "paddingAll": "15px",
                    "cornerRadius": "md",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "قراءة العلاقات",
                            "weight": "bold",
                            "size": "md",
                            "color": "#BA55D3"
                        },
                        {
                            "type": "text",
                            "text": "لفهم علاقاتك العاطفية",
                            "size": "xs",
                            "color": "#999999",
                            "margin": "xs"
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#BA55D3",
                            "action": {
                                "type": "postback",
                                "label": "ابدأ القراءة",
                                "data": "action=reading&type=relationship"
                            },
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#F8E6FF",
                    "paddingAll": "15px",
                    "cornerRadius": "md",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "قراءة القرار",
                            "weight": "bold",
                            "size": "md",
                            "color": "#9932CC"
                        },
                        {
                            "type": "text",
                            "text": "للمساعدة في اتخاذ القرارات",
                            "size": "xs",
                            "color": "#999999",
                            "margin": "xs"
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#9932CC",
                            "action": {
                                "type": "postback",
                                "label": "ابدأ القراءة",
                                "data": "action=reading&type=decision"
                            },
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#EDE6F5",
                    "paddingAll": "15px",
                    "cornerRadius": "md",
                    "margin": "md"
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "action": {
                        "type": "postback",
                        "label": "العودة للقائمة الرئيسية",
                        "data": "action=main_menu"
                    }
                }
            ],
            "paddingAll": "15px"
        }
    }

def create_card_display(card, is_daily=False):
    """عرض بطاقة واحدة"""
    direction = "معكوسة" if card['reversed'] else "مستقيمة"
    meaning = card['meaning_reversed'] if card['reversed'] else card['meaning_upright']
    
    return {
        "type": "bubble",
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "بطاقة اليوم" if is_daily else "بطاقتك",
                    "weight": "bold",
                    "size": "sm",
                    "align": "center",
                    "color": "#FFFFFF"
                },
                {
                    "type": "text",
                    "text": card['name_ar'],
                    "weight": "bold",
                    "size": "xxl",
                    "align": "center",
                    "color": "#FFFFFF",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": card['name'],
                    "size": "sm",
                    "align": "center",
                    "color": "#FFFFFF",
                    "margin": "xs"
                },
                {
                    "type": "text",
                    "text": f"({direction})",
                    "size": "xs",
                    "align": "center",
                    "color": "#FFD700",
                    "margin": "sm"
                }
            ],
            "paddingAll": "25px",
            "backgroundColor": card.get('color', '#8B4789')
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "المعنى",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#8B4789"
                },
                {
                    "type": "text",
                    "text": meaning,
                    "size": "sm",
                    "wrap": True,
                    "color": "#555555",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "الكلمات المفتاحية",
                    "weight": "bold",
                    "size": "md",
                    "color": "#8B4789",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": " | ".join(card['keywords']),
                    "size": "sm",
                    "wrap": True,
                    "color": "#9370DB",
                    "margin": "sm"
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#9370DB",
                    "action": {
                        "type": "postback",
                        "label": "قراءة جديدة",
                        "data": "action=reading_menu"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "action": {
                        "type": "postback",
                        "label": "القائمة الرئيسية",
                        "data": "action=main_menu"
                    },
                    "margin": "sm"
                }
            ],
            "paddingAll": "15px"
        }
    }

def create_spread_result(result):
    """عرض نتيجة قراءة متعددة البطاقات"""
    cards = result['cards']
    
    # إنشاء محتويات البطاقات
    cards_contents = []
    
    positions = {
        'past_present_future': ['الماضي', 'الحاضر', 'المستقبل'],
        'relationship': ['أنت', 'الطرف الآخر', 'العلاقة'],
        'decision': ['الخيار الأول', 'الخيار الثاني']
    }
    
    position_labels = positions.get(result['type'], [f'البطاقة {i+1}' for i in range(len(cards))])
    
    for i, card in enumerate(cards):
        direction = "معكوسة" if card['reversed'] else "مستقيمة"
        
        if i > 0:
            cards_contents.append({
                "type": "separator",
                "margin": "lg"
            })
        
        cards_contents.extend([
            {
                "type": "text",
                "text": position_labels[i],
                "weight": "bold",
                "size": "md",
                "color": "#8B4789",
                "margin": "lg" if i > 0 else "none"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": card['name_ar'],
                        "size": "sm",
                        "weight": "bold",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": f"({direction})",
                        "size": "xs",
                        "color": "#999999",
                        "align": "end"
                    }
                ],
                "margin": "xs"
            },
            {
                "type": "text",
                "text": " | ".join(card['keywords'][:3]),
                "size": "xs",
                "color": "#9370DB",
                "margin": "xs"
            }
        ])
    
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": result['title'],
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "color": "#FFFFFF"
                },
                {
                    "type": "text",
                    "text": datetime.fromisoformat(result['timestamp']).strftime("%Y-%m-%d %H:%M"),
                    "size": "xs",
                    "align": "center",
                    "color": "#FFFFFF",
                    "margin": "sm"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#8B4789"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": cards_contents + [
                {
                    "type": "separator",
                    "margin": "xl"
                },
                {
                    "type": "text",
                    "text": "التفسير",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#8B4789",
                    "margin": "xl"
                },
                {
                    "type": "text",
                    "text": result['interpretation'],
                    "size": "sm",
                    "wrap": True,
                    "color": "#555555",
                    "margin": "md"
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#9370DB",
                    "action": {
                        "type": "postback",
                        "label": "قراءة جديدة",
                        "data": "action=reading_menu"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "action": {
                        "type": "postback",
                        "label": "القائمة الرئيسية",
                        "data": "action=main_menu"
                    },
                    "margin": "sm"
                }
            ],
            "paddingAll": "15px"
        }
    }

def create_history_view(history):
    """عرض سجل القراءات"""
    if not history:
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "لا يوجد سجل قراءات",
                        "align": "center",
                        "color": "#999999",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": "ابدأ قراءة جديدة الآن",
                        "align": "center",
                        "color": "#999999",
                        "size": "sm",
                        "margin": "md"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#9370DB",
                        "action": {
                            "type": "postback",
                            "label": "بدء قراءة",
                            "data": "action=reading_menu"
                        },
                        "margin": "lg"
                    }
                ],
                "paddingAll": "40px"
            }
        }
    
    # عرض آخر 5 قراءات فقط
    history_contents = []
    
    for i, reading in enumerate(history[:5]):
        if i > 0:
            history_contents.append({
                "type": "separator",
                "margin": "lg"
            })
        
        timestamp = datetime.fromisoformat(reading['timestamp']).strftime("%d/%m/%Y %H:%M")
        cards_summary = f"{len(reading['cards'])} بطاقة"
        
        history_contents.extend([
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": reading['title'],
                        "weight": "bold",
                        "size": "sm",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": timestamp,
                        "size": "xs",
                        "color": "#999999",
                        "align": "end"
                    }
                ],
                "margin": "lg" if i > 0 else "none"
            },
            {
                "type": "text",
                "text": cards_summary,
                "size": "xs",
                "color": "#9370DB",
                "margin": "xs"
            }
        ])
    
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "سجل القراءات",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "color": "#FFFFFF"
                },
                {
                    "type": "text",
                    "text": f"آخر {len(history[:5])} قراءات",
                    "size": "xs",
                    "align": "center",
                    "color": "#FFFFFF",
                    "margin": "sm"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#8B4789"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": history_contents,
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#9370DB",
                    "action": {
                        "type": "postback",
                        "label": "قراءة جديدة",
                        "data": "action=reading_menu"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "action": {
                        "type": "postback",
                        "label": "القائمة الرئيسية",
                        "data": "action=main_menu"
                    },
                    "margin": "sm"
                }
            ],
            "paddingAll": "15px"
        }
    }
