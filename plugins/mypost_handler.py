from pyrogram import Client, filters, types
from pyrogram.types import (
    InlineKeyboardMarkup as markup,
    InlineKeyboardButton as button,
)
from utils import load_from_db


@Client.on_callback_query(filters.regex("^my_posts"))
async def my_posts(_, cb: types.CallbackQuery):
    user = cb.from_user
    await cb.message.delete()
    data = load_from_db(user.id)
    if not data:
        return await cb.message.reply("You have no posts")
    for _, data in data.items():
        if data["taken"]:
            continue
        text = f"""Name: **{data["name"]}**
Item Description: **{data["item"]}**
Price: **{data["price"]}**"""
        await cb.message.reply(
            text,
            reply_markup=markup(
                [
                    [
                        button("Mark Taken", f"taken_{data['message_id']}_{user.id}"),
                    ]
                ]
            ),
        )
