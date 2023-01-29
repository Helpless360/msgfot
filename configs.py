from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    def __init__(self):
        self._api_id = os.getenv('API_ID', "0")
        self._api_hash = os.getenv('API_HASH', "0")
        self._bot_token = os.getenv('BOT_TOKEN', "0")
        self._owner_id = os.getenv('OWNER_ID', "0")
        self._channel_id = os.getenv('CHANNEL_ID', "0")
        self._version = "1.0.0"

    @property
    def api_id(self):
        return int(self._api_id)

    @property
    def api_hash(self):
        return self._api_hash

    @property
    def bot_token(self):
        return self._bot_token

    @property
    def owner_id(self):
        return int(self._owner_id)

    @property
    def version(self):
        return self._version

    @property
    def channel_id(self):
        return int(self._channel_id)


configs = Config()
