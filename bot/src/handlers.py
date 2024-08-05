from aiogram import Dispatcher, html, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from src.kb import KB
from src.depends import get_service


router = Router()

@router.message(Command('help'))
async def help_handler(message: Message):
    await message.answer("Вы можете создать сообщение или получить список всех сообщений.")
    await message.answer(
"""Список доступных команд:
1./create - Введите эту команду и сообщение следом за ней для создания сообщения.\n
2. /get_all - Возвращает список всех сообщений в сортированном порядке.""", reply_markup=KB.keyboard_help)
    

@router.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    await message.answer(f'''Привет, {html.bold(message.from_user.full_name)}. 
Это тестовое задание, выполненное {html.bold('Максимом Кривоносовым')}. Наберите /help для получения большей информации.''', reply_markup=KB.keyboard_start)
    
@router.message(Command('get_all'))
async def get_all_messages_handler(message: Message):
    service = get_service()
    
    messages: str = await service.get_message_list()
    
    if messages is None:
        await message.answer('Не удалось получить список сообщений, попробуйте еще раз позже.')
        return
    
    await message.answer(messages)
    
    

@router.message(Command('create'))
async def create_message_handler(message: Message):
    service = get_service()
    
    try:
        rsp = await service.send_message_to_server(message)
    except ValueError:
        await message.answer('Добавьте свое сообщение после /create, поле не может быть пустым.')
        return
    
    
    if rsp is not None:
        await message.answer(rsp)
    else:
        await message.answer('Не удалось создать сообщение в базе данных, попробуйте позже.')
    



@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.answer('К сожалению, я пока еще не знаю такой команды :(')
    except TypeError:
        await message.answer("Неподдерживаемый тип сообщения :(")



