from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Меню
btn_show = KeyboardButton('Показать заполненные баки')
btn_info = KeyboardButton('Показать все баки')
btn_spam = KeyboardButton('Оповещения')
menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_show, btn_info, btn_spam)

# Рассылка
inline_button_yes = InlineKeyboardButton('Да', callback_data='yes')
inline_button_off = InlineKeyboardButton('Хочу отключить рассылку', callback_data='off')
spam_message = InlineKeyboardMarkup().add(inline_button_yes, inline_button_off)

# Меню рассылки
inline_button_all = InlineKeyboardButton('О всех', callback_data='all')
inline_button_several = InlineKeyboardButton('О нескольких', callback_data='several')
spam_menu = InlineKeyboardMarkup().add(inline_button_all, inline_button_several)

# Меню выбора рассылки

spam_choise = InlineKeyboardMarkup()
