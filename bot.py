from email.mime import image
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from database import *
import os
from tiktok import *
load_dotenv()


admin=False
TOKEN = os.getenv('TOKEN')
bot = Bot(token = TOKEN, parse_mode = types.ParseMode.HTML)

dp = Dispatcher(bot)

@dp.message_handler(commands = ['start'])
async def cmd_start(message: types.Message):
    await add_user(message)
    
@dp.message_handler(commands = ['help'])
async def cmd_help(message: types.Message):
    await message.answer('<b>Tik Tok</b> - tiktok bot video yuklab olish uchun tiktok video linkini kiriting\n<b>/help</b> - bot haqida malumot olish uchun')
    

@dp.message_handler(content_types = ['text'])
async def on_text_message(message: types.Message):
    if message.text.lower()=='ассалом алейкум'\
        or message.text.lower() =='salom alaykum' or message.text.lower()=='salom'\
        or message.text.lower()=='салом' or message.text.lower()=='assalom alaykum':
            await message.reply('Salom <b>{}</b>!'.format(message.from_user.full_name))
    elif message.text.lower()=='привет' or message.text.lower()=='здравствуй' or message.text.lower()=='здравствуйте':
            await message.reply('привет <b>{}</b>!'.format(message.from_user.full_name))
            
    
    # Admin Panel
    elif message.text.lower()=='admin123':
        global admin
        admin=True
    # TikTok Video Download  
    else:
        for entity in message.entities:
            if entity.type in ["url", "text_link"]:
                await tiktok(message,os.getenv('HOST'),os.getenv('KEY'))
                break
            

@dp.message_handler(content_types=['sticker'])
async def on_sticker_message(message: types.Message):
    await message.reply_sticker(sticker = 'CAACAgIAAxkBAAIF9mKGqGLTia1bSVlYA1fK-lGHrLYkAALPAAP3AsgPufg4-6cYrv0kBA')



@dp.message_handler(content_types=['photo'])
async def on_photo_message(message: types.Message):
    if admin:
        user= await get_user()
        for i in user.fetchall():
            await bot.send_photo(i[1],photo=message.photo[-1].file_id,caption=message.caption)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    db.close()

