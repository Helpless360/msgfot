from pyrogram import Client
from configs import configs

bot = Client(
    "bot",
    configs.api_id,
    configs.api_hash,
    bot_token=configs.bot_token,
    plugins=dict(root="plugins")
)
