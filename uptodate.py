"""
MIT License

Copyright (c) 2021 Tinura Dinith

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers.sql import add_user, remove_user, user_list, count_users
from config import BOT_TOKEN, SUDO, ACAST, CHANNELS

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def startmsg(message):
    await bot.send_photo(message.chat.id, photo="https://telegra.ph/file/6ba8edad2c30969e5171a.jpg",
    caption="""
Hello, I'm official bot of @uptodatelk 🇱🇰

You can get all tech news that post by @uptodatelk channel by using me.
""", 
    reply_markup=InlineKeyboardMarkup()
                .add(InlineKeyboardButton("News 🖥", url="https://t.me/uptodatelk"),
                     InlineKeyboardButton("Discussion 💬", url="https://t.me/uptodatechat")))
    if message.chat.type == "private":
        add_user(message.from_user.id, message.from_user.first_name)                 

@dp.message_handler(commands="stats")
async def statics(message):
    if not message.from_user.id in SUDO:
     return
    if message.from_user.id in SUDO:
      await message.reply(f"Total Users - {count_users()}")

@dp.message_handler(commands="cast")
async def castmsgs(message):
   if message.reply_to_message:
    users = user_list()
    success = 0
    failed = 0
    for user in users:
       try: 
        chat_id = int(user[0])
        await message.reply_to_message.send_copy(chat_id=chat_id)
        success += 1
       except:
        remove_user(chat_id)
        failed += 1
    await message.reply(f"""
Casting Finished ✅

Methond - Manually by {message.from_user.mention}
Success - {str(success)}
Failed - {str(failed)}
    """)     

@dp.channel_post_handler()
async def autocast(message):
   if message.chat.id not in CHANNELS:
       return await bot.leave_chat(message.chat.id)
   if ACAST and message.chat.id in CHANNELS:
    users = user_list()
    success = 0
    failed = 0
    for user in users:
       try: 
        chat_id = int(user[0])
        await message.send_copy(chat_id=chat_id)
        success += 1
       except:
        remove_user(chat_id)
        failed += 1
    for sudo in SUDO:
     await bot.send_message(int(sudo),f"""
Casting Finished ✅

Methond - Autocasting
Link - {message.url}
Success - {str(success)}
Failed - {str(failed)}
    """)     

@dp.message_handler(commands="stop")
async def startmsg(message):
    await bot.send_message(message.chat.id, text="You have unsubscribed our news service, I will not send messages to you until you use me again.")
    if message.chat.type == "private":
        remove_user(message.from_user.id)   

print("Uptodatelk Bot started.")
executor.start_polling(dp)
