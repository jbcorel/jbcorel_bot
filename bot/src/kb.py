
from aiogram import types

class KB:
    
    all_commands = [[
        types.KeyboardButton(text='/help'),
        types.KeyboardButton(text='/create'),
        types.KeyboardButton(text='/get_all'),
    ],]
    
    help = [[
        types.KeyboardButton(text='/help')
    ],]
    
    keyboard_help = types.ReplyKeyboardMarkup(
        keyboard= all_commands,
        resize_keyboard=True,
        input_field_placeholder='Доступные команды'
    )
    
    keyboard_start = types.ReplyKeyboardMarkup(
        keyboard=help,
        resize_keyboard=True,
        input_field_placeholder='Help!!!'
    )