import os
from dotenv import load_dotenv
import vk_api
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker


class VKBotConnection:

    def __init__(self):
        load_dotenv()
        self.token = os.getenv('MY_VK_GROUP_TOKEN')
        self.vk_session = VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk_session)


class VKUserConnection:

    def __init__(self):
        load_dotenv()
        self.token = os.getenv('MY_VK_APP_TOKEN')
        self.vk_session = VkApi(token=self.token)


class DataBaseConnection:

    def __init__(self):
        load_dotenv()
        self.DSN = os.getenv('DSN')
        self.engine = sq.create_engine(self.DSN, echo=True)
        self.session = sessionmaker(bind=self.engine)
