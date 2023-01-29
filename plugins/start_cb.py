import json
import os
from pyrogram import Client, filters, types
from utils import convs, get_conv, save_to_db, load_from_db, send_to_channel
from pyrogram.types import (
    InlineKeyboardMarkup as markup,
    InlineKeyboardButton as button,
)
from configs import configs

infos = {}


@Client.on_callback_query(filters.regex("^start_post$"))
async def start_post(_, c: types.CallbackQuery):
    text = """**What is your name**:
(Note: this will appear in the main channel)"""
    await c.message.reply(text)
    infos[c.from_user.id] = {}
    convs[c.from_user.id] = "name"


@Client.on_message(filters.private & get_conv("name"))
async def name(_, m: types.Message):
    text = """**Item name**:
(Eg. Calculator, crop top)"""
    await m.reply(text)
    infos[m.from_user.id]["name"] = m.text
    convs[m.from_user.id] = "item"


@Client.on_message(filters.private & get_conv("item"))
async def item(_, m: types.Message):
    text = "**Price** (Include postage):"
    await m.reply(text)
    infos[m.from_user.id]["item"] = m.text
    convs[m.from_user.id] = "price"


@Client.on_message(filters.private & get_conv("price"))
async def price_hndlr(_, m: types.Message):
    if not m.text:
        return await m.reply("Please send a valid price")
    text = "**Please send me 1 photo of the item**"
    await m.reply(text)
    infos[m.from_user.id]["price"] = m.text
    convs[m.from_user.id] = "photo"


@Client.on_message(filters.private & get_conv("photo"))
async def photo(_, m: types.Message):
    if not m.photo:
        return await m.reply("Please send me a photo")
    phhto = await m.download()
    infos[m.from_user.id]["photo"] = phhto
    description = f"""**Name**: {infos[m.from_user.id]["name"]}
**Item Description**: {infos[m.from_user.id]["item"]}
**Price**: {infos[m.from_user.id]["price"]}
**Telegram Contact**: @{m.from_user.username}"""
    text = f"""**Okay, please confirm your posting**:
{description}
"""
    infos[m.from_user.id]["text"] = description
    await m.reply(
        text,
        reply_markup=markup(
            [
                [
                    button("Confirm", "confirm"),
                ],
                [
                    button("Cancel", "cancel"),
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("^reset$"))
async def reset(c: Client, cb: types.CallbackQuery):
    user_id = cb.from_user.id

    try:
        os.remove(f"db/data_{user_id}.json")
    except Exception as e:
        print(e)

    await cb.message.reply("All your data has been reset")
    await cb.message.delete()


@Client.on_callback_query(filters.regex("^confirm$"))
async def confirm(c: Client, cb: types.CallbackQuery):
    text = """Yayyy! Your post has been posted to the channel.
Don't forget to click **Mark Taken** button when somebody have collected your item!"""
    infos[cb.from_user.id]["taken"] = False
    await cb.edit_message_reply_markup(reply_markup=None)
    x = await send_to_channel(
        c, infos[cb.from_user.id], infos[cb.from_user.id]["text"], cb
    )
    infos[cb.from_user.id]["message_id"] = x
    infos[cb.from_user.id]["report"] = {
        "reporters": [],
        "count": 0,
    }

    save_to_db(cb.from_user.id, infos[cb.from_user.id], x)
    await cb.message.reply(
        text,
        reply_markup=markup(
            [
                [button("Home", "home")],
                [button("Go To Your Post", url=f"https://t.me/c/{str(configs.channel_id)[4:]}/{x}")],
            ],
        )
    )
    del infos[cb.from_user.id]
    del convs[cb.from_user.id]
