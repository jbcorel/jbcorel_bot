import aiohttp
from src.service import ServerConnectionService
from src.config import Config


session: aiohttp.ClientSession = None  

service: ServerConnectionService = None


async def init_session():
    global session
    session = aiohttp.ClientSession(base_url=Config.API_URL, raise_for_status=True)


async def init_service():
    global service
    service = ServerConnectionService(get_session())


def get_service():
    global service
    return service


def get_session():
    global session
    return session


async def close_session():
    global session
    if session is not None:
        await session.close()
        session = None
        print('-------------------')
        print ('Session is closed now')