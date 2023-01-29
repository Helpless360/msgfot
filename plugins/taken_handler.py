from pyrogram import Client, filters, types
from pyrogram.types import (
    InlineKeyboardMarkup as markup,
    InlineKeyboardButton as button,
)
from utils import load_from_db, save_to_db
from configs import configs


@Client.on_callback_query(filters.regex(r"^taken_(\d+)_(\d+)$"))
async def taken(c: Client, cb: types.CallbackQuery):
    user = cb.from_user
    data = load_from_db(user.id)
    if not data:
        return await cb.message.reply("You have no posts")
    message_id = int(cb.matches[0].group(1))
    if user.id != int(cb.matches[0].group(2)):
        return await cb.message.reply("You are not the owner of this post")
    for dat in data:
        if data[dat]["message_id"] != message_id:
            continue

        data[dat]["taken"] = True
        
        save_to_db(user.id, data[dat], message_id)
        message_text = await c.get_messages(configs.channel_id, message_id)
        if message_text.empty:
            await cb.message.reply("This post has been deleted already either by admin or its reported")
            await cb.message.delete()
            return
        
        await message_text.edit_caption(
            caption=f"{message_text.caption}.",
            reply_markup=markup(
                [[button("Taken", callback_data="sorry_taken")]]
            ),
        )

        reply_markup=markup(
            [
                [button("Home", "home")],
            ],
        )

        # save_to_db(user.id, dat, message_id)
        await cb.message.reply("Marked as taken", reply_markup=reply_markup)
        await cb.message.delete()
        break


@Client.on_callback_query(filters.regex("^sorry_taken$"))
async def sorry_taken(_, cb: types.CallbackQuery):
    return await cb.answer("Sorry, this post is already taken", show_alert=True)
