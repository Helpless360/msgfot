from pyrogram import Client, filters, types
from utils import load_from_db, save_to_db
from configs import configs


@Client.on_callback_query(filters.regex(r"^report_(\d+)$"))
async def report(c: Client, cb: types.CallbackQuery):
    user = cb.from_user
    user_id = int(cb.matches[0].group(1))
    datas = load_from_db(user_id)
    if not datas:
        return await cb.message.reply("You have no posts")
    message_id = cb.message.id
    for _, data in datas.items():
        if data["message_id"] != message_id:
            continue
        if user.id in data["report"]["reporters"]:
            return await cb.answer("You have already reported this post", show_alert=True)
        data["report"]["reporters"].append(user.id)
        data["report"]["count"] += 1

        save_to_db(user.id, datas[str(message_id)], message_id)
        if data["report"]["count"] == 2:
            await c.delete_messages(configs.channel_id, message_id)
            await c.send_message(
                user_id,
                "Your post has been deleted because it was reported twice",
            )
            del datas[str(data["message_id"])]
            save_to_db(user.id, datas[str(message_id)], message_id)
            return await cb.message.delete()
        await cb.answer("Reported", show_alert=True)
        break
