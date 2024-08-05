import aiohttp
from aiogram.types import Message
from datetime import datetime

class ServerConnectionService:
    
    post_api_url = '/api/v1/message'
    get_api_url = '/api/v1/messages'
    
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session
        
        
    async def send_message_to_server(self, message: Message) -> dict:
        author = message.from_user.full_name
        date = message.date 
        content = message.text[7:]
        if not content:
            raise ValueError('Сообщение не может быть пустым')
        
        payload = {
            'author': author,
            'date_created': date.isoformat(),
            'content': content
        }
        
        try:
            async with self.session.post(self.post_api_url, json=payload) as rsp:
                    rsp.raise_for_status()
                    if rsp.status == 201:
                        rsp = await rsp.json()
                        return self.parse_message(rsp['data'][0])
        except Exception as e:
            print (e)
            return


    async def get_message_list(self):
        try:
            async with self.session.get(self.get_api_url) as rsp:
                rsp.raise_for_status()
                if rsp.status == 200:
                    rsp = await rsp.json()
                    return self.parse_message_list(rsp['data'])
        except Exception as e:
            print (e)
            return
    
    def parse_message(self, message: dict):
        try:
            date = datetime.fromisoformat(message['date_created'])
            formatted = date.strftime('%a %d %b %Y, %I:%M%p')
            s = 'Автор: {}\nТекст: {}\nВремя создания: {} (UTC)'\
                    .format(message['author'], message['content'], formatted)
                
            return s 
        
        except Exception as e: 
            print(e)
            return 
        
        
    def parse_message_list(self, lst: list) -> str:
        try:
            s = ''
            for obj in lst:
                date = datetime.fromisoformat(obj['date_created'])
                formatted = date.strftime('%a %d %b %Y, %I:%M%p')
                
                obj_str = "\nАвтор: {}\nТекст: {}\nВремя создания: {} (UTC)\n" \
                        .format(obj['author'], obj['content'], formatted)
                    
                s = s + obj_str
                
            return s if s else 'Еще нет сообщений, создайте!'
        except Exception as e:
            print(e)
            return