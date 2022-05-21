
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from database.db import *
import os

from download.tiktok import *
from download.instagram import *
load_dotenv()

channels=['@masteruzdev']

admins=[]


TOKEN = os.getenv('TOKEN')
bot = Bot(token = TOKEN, parse_mode = types.ParseMode.HTML)

dp = Dispatcher(bot)

@dp.message_handler(commands = ['start'])
async def cmd_start(message: types.Message):
    await add_user(message)
   
    
@dp.message_handler(commands = ['help'])
async def cmd_help(message: types.Message):
    await message.answer('<b>Tik Tok</b> - tiktok va instagram download bot video va photo yuklab olish uchun linkini \
        kiriting\n<b>/help</b> - bot haqida malumot olish uchun')
    

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
        admins.append(message.from_user.id)
    # TikTok Video Download  
    else:
        for entity in message.entities:
            if entity.type in ["url", "text_link"]:
                
                try:
                    for channel in channels:
                        global status
                        status = await bot.get_chat_member(channel, message.chat.id)
                
                    # channel 
                    if status['status']=='member' or status['status']=='creator' or status['status']=='administrator':
                        if message.text.lower().startswith('https://www.tiktok.com/'):
                            await tiktok(message,os.getenv('THOST'),os.getenv('TKEY'),os.getenv('TURL'))
                            break
                        elif message.text.lower().startswith('https://www.instagram.com/p/'):
                            await instagram(message,os.getenv('YHOST'),os.getenv('YKEY'),os.getenv('YURL'))
                            break
                        else:
                            await message.reply('<b>{}</b> - tiktok va instagram video yuklanmadi qaytib link ni tug\'riligini tekshirib ko\'ring'.format(message.text))
                            #breaklogin_url=types.LoginUrl(url='https://t.me/{}'.format(channel))
                            break
                    else:
                        
                        button =types.InlineKeyboardButton(text='Kanalga obuna bul', callback_data='1', login_url=types.LoginUrl(url='https://t.me/python_node_aiogram_telegraf_bot'))
                        key=types.InlineKeyboardMarkup().insert(button)
                        await bot.send_message(message.chat.id,
                            'Kanalga obuna bulmagansiz <b>{}</b> \n bu botdan foydalanish uchun kanalga obuna buling'.format(message.from_user.full_name),
                            reply_markup=key
                        )
                except:
                    button =types.InlineKeyboardButton(text='Botga uting', callback_data='1', url='https://t.me/python_node_aiogram_telegraf_bot')
                    key = types.InlineKeyboardMarkup().insert(button)
                    await message.reply('<b>{}</b> - botga uting va linkni tashlang'.format(message.text),reply_markup=key)
            else:
                pass
            
                    
@dp.message_handler(content_types=['sticker'])
async def on_sticker_message(message: types.Message):
    await message.reply_sticker(sticker = 'CAACAgIAAxkBAAIF9mKGqGLTia1bSVlYA1fK-lGHrLYkAALPAAP3AsgPufg4-6cYrv0kBA')



@dp.message_handler(content_types=['photo'])
async def on_photo_message(message: types.Message):
    for admin in admins:
        if admin==message.from_user.id:
            user= await get_user()
            for i in user.fetchall():
                await bot.send_photo(i[1],photo=message.photo[-1].file_id,caption=message.caption,parse_mode='HTML',disable_notification=True)
            break
        else:
            pass

@dp.callback_query_handler()
async def on_callback_query(callback_query: types.CallbackQuery):
    if callback_query.data=='1':
        await callback_query.answer('kanalga obuna buling',show_alert=True)
    
    
@dp.message_handler(content_types=["new_chat_members"])
async def on_new_chat_member(message: types.Message):
    await message.delete()
        
    await message.answer('<b>{}</b> - Guruhga hush kelibsiz'.format(message.from_user.full_name))
       
@dp.message_handler(content_types=["left_chat_member"])
async def on_left_chat_member(message: types.Message):
    await message.delete()

@dp.message_handler(content_types=["new_chat_title"])
async def on_new_chat_title(message: types.Message):
    await message.delete()
    print(message.new_chat_title)
@dp.message_handler(content_types=["new_chat_photo"])
async def on_new_chat_photo(message: types.Message):
    await message.delete()
    print(message.new_chat_photo)
@dp.message_handler(content_types=["delete_chat_photo"])
async def on_delete_chat_photo(message: types.Message):
    await message.delete()
    print(message.delete_chat_photo)
    
# pin
# @dp.message_handler(content_types=["new_chat_pinned_message"])
# async def on_new_chat_pinned_message(message: types.Message):
#     await message.delete()

@dp.message_handler(content_types=["pinned_message"])
async def on_pinned_message(message: types.Message):
    await message.delete()
    print(message.pinned_message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    db.close()

