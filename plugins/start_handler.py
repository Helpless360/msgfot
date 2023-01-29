from pyrogram import Client, filters, types
from pyrogram.types import (
    InlineKeyboardMarkup as markup,
    InlineKeyboardButton as button,
)
from utils import load_from_db


@Client.on_callback_query(filters.regex("^home$"))
@Client.on_message(filters.command("start"))
async def start_func(_, m: types.Message | types.CallbackQuery):
    user = m.from_user
    if not user.username:
        return await m.reply("Please set your username in telegram settings to use this.")
    if isinstance(m, types.CallbackQuery):
        m = m.message
        await m.delete()
    keyboard = [
        [
            button("💻 Start Post", "start_post"),
        ],
        [button("Listing Channel", url="https://t.me/sgthrifting")],
    ]
    if data := load_from_db(user.id):

        if any(not data[i]["taken"] for i in data):
            keyboard[0].insert(1, button("📒 My Posts", "my_posts"))
            keyboard[1].insert(1, button("Reset Account", "reset"))

    text = "Hello everyone :) ! Welcome to Singapore Thrifting Telegram Channel! Our goal is to reduce waste by creating a common platform that allow users to thrift unwanted items easily. Sell cheap / give away (p&h). List item through this bot. Ensure that you have a telegram handle else the bot will not work."

    return await m.reply(
        text,
        reply_markup=markup(keyboard),
    )
