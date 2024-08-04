
from aiogram import types

class KB:
    
    all_commands = [[
        types.KeyboardButton(text='/help'),
        types.KeyboardButton(text='/create_message'),
        types.KeyboardButton(text='/get_all_messages'),
    ],]
    
    essential = [[
        types.KeyboardButton(text='Создать сообщение'),
        types.KeyboardButton(text='Получить список сообщений')
    ],]
    
    
    start = [[
        types.KeyboardButton(text='/start'),
    ],]
    
    keyboard_start = types.ReplyKeyboardMarkup(
        keyboard= all_commands,
        resize_keyboard=True,
        input_field_placeholder='Доступные команды'
    )
    