import json
import os
import traceback
from pyrogram import filters, Client, types
from configs import configs
from pyrogram.types import InlineKeyboardMarkup as markup, InlineKeyboardButton as button

convs = {}


def get_conv(level: str):
    async def func(_, __, m):
        return convs.get(m.from_user.id) == level
    return filters.create(func, "ConvHandler")


def save_to_db(user_id, datas, message_id):
    if os.path.exists(f"db/data_{user_id}.json"):
        with open(f"db/data_{user_id}.json", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
            if str(message_id) not in data:
                data[str(message_id)] = {}

            try:
                data[str(message_id)].update(datas)
            except KeyError:
                traceback.print_exc()
    else:
        data = {message_id: datas}

    with open(f"db/data_{user_id}.json", "w") as f:
        json.dump(data, f, indent=2)
    with open(f"db/data_{user_id}.json", "r") as f:
        return json.load(f)


def load_from_db(user_id) -> dict:
    try:
        with open(f"db/data_{user_id}.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
    except FileNotFoundError:
        return {}


async def send_to_channel(c: Client, data: dict, text: str, cb: types.CallbackQuery):
    if not configs.channel_id:
        return await cb.message.reply("Please set the channel id in configs.py")
    text = f"""New Listing on @sgthrifting
{text}

Note: Love this channel? Share it with your friend today!"""
    try:
        x = await c.send_photo(
            chat_id=configs.channel_id,
            photo=data["photo"],
            caption=text,
            reply_markup=markup(
                [
                    [
                        button(f"Contact {cb.from_user.first_name}", url=f"https://t.me/{cb.from_user.username}"),
                        button("Report", f"report_{cb.from_user.id}"),
                    ]
                ]
            )
        )
        return x.id
    except Exception as e:
        await cb.message.reply(f"Error: {e}")
