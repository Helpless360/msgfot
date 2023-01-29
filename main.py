import os
from clients import bot
from pyrogram import idle


async def main():
    if not os.path.exists("db"):
        os.mkdir("db")
    print(">>> Database Connected!")
    print(">>> Starting Bot...")
    await bot.start()
    print(">>> Bot Started!")
    print(
        f"""Name: {bot.me.first_name}
ID: {bot.me.id}
Username: @{bot.me.username}"""
    )
    print(">>> Bot Idle...")
    await idle()
    print(">>> Bot Stopped!")
    await bot.stop()


if __name__ == "__main__":
    bot.run(main())
