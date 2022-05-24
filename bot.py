from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
from download import *
from database import *

load_dotenv()

channels=['@masteruzdev']

admins=[]

logging.basicConfig(filename='bot.log',level=logging.ERROR,filemode='a')

TOKEN = os.getenv('TOKEN')
bot = Bot(token = TOKEN, parse_mode = types.ParseMode.HTML)

dp = Dispatcher(bot)

@dp.message_handler(commands = ['start'])
async def cmd_start(message: types.Message):
    await add_user(message)
    

    
@dp.message_handler(commands = ['count'])
async def cmd_count(message: types.Message):
    for admin in admins:
        if admin == message.from_user.id:
            await message.answer(f'🔰 Botga qo\'shilgan foydalanuvchilar soni - <b>{await count_user()}👥</b>')
            break

@dp.message_handler(commands = ['admins'])
async def cmd_admins(message: types.Message):
    for admin in admins:
        if admin == message.from_user.id:
            await message.answer(f'👨🏻‍💻 Bot administratorlar soni - <b>{len(admins)}👤</b>')
            break

@dp.message_handler(commands = ['logs'])
async def cmd_logs(message: types.Message):
    for admin in admins:
        if admin == message.from_user.id:
            try:
                with open('bot.log','r') as file:
                    await message.answer('Error: 👁‍🗨\n\n',file.read())
                    break
            except Exception as warning:
                # logging.warning(f'Log: {warning}')
                print('Log: ',warning)
                await message.answer('Error: 👁‍🗨\n\n',warning)

@dp.message_handler(commands = ['help'])
async def cmd_help(message: types.Message):
    
    for admin in admins:
        if admin == message.chat.id:
            await message.answer(
                '<b>Bot administratorlar uchun:\n</b>👨🏻‍💻/admins - Adminlar soni\n🔰/count - Foydalanuvchilar soni\n🚫/logs - Bot loglarini olish \n\n '
            )
            break
        
    await message.answer(
        '<b>Tik-Tok | Instagram Download</b> - tiktok va instagram download bot vedio va photo yuklab olish uchun linkini kiriting <b>⬇️</b>'
    )
        
            
@dp.message_handler(content_types = ['text'])
async def on_text_message(message: types.Message):
    
    
    if message.text.lower() == 'ассалом алейкум'\
        or message.text.lower() =='salom alaykum' or message.text.lower() == 'salom'\
        or message.text.lower() == 'салом' or message.text.lower() == 'assalom alaykum':
            await message.reply('Salom <b>{}</b>!'.format(message.from_user.full_name))
    elif message.text.lower() == 'привет' or message.text.lower() == 'здравствуй' or message.text.lower() == 'здравствуйте':
            await message.reply('привет <b>{}</b>!'.format(message.from_user.full_name))
            
    
    # Admin Panel
    elif message.text.lower() == 'admin123':
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
                    if status['status'] == 'member' or status['status'] == 'creator' or status['status'] == 'administrator':
                        if message.text.lower().startswith('https://www.tiktok.com/'):
                            await tiktok(message,os.getenv('THOST'),os.getenv('TKEY'),os.getenv('TURL'),logging)
                            break
                        elif message.text.lower().startswith('https://www.instagram.com/'):
                            await instagram(message,os.getenv('YHOST'),os.getenv('YKEY'),os.getenv('YURL'))
                            break
                        else:
                            await message.reply('<b>{}</b> - tiktok va instagram video yuklanmadi qaytib link ni tug\'riligini tekshirib ko\'ring'.format(message.text))
                            break
                    else:
                        
                        button = types.InlineKeyboardButton(text = '🔗 Kanalga obuna buling 🔗', url = 'https://t.me/masteruzdev')
                        markup = types.InlineKeyboardMarkup()
                        markup.add(button)
                        await message.reply('<b>{}</b> - Kanalga obuna buling'.format(message.text), reply_markup = markup)
                except Exception as error:
                    logging.error(f'Bot File: {error}')
                    button = types.InlineKeyboardButton(text = '🔗 Botga Utish 🔗', url = 'https://t.me/instagram_tiktok_download_bot')
                    markup = types.InlineKeyboardMarkup().insert(button)
                    await message.reply('<b>{}</b> - Botga utinb linkni tashlang '.format(message.text),reply_markup = markup)
            
                    
@dp.message_handler(content_types = ['sticker'])
async def on_sticker_message(message: types.Message):
    await message.reply_sticker(sticker = 'CAACAgIAAxkBAAIF9mKGqGLTia1bSVlYA1fK-lGHrLYkAALPAAP3AsgPufg4-6cYrv0kBA')


album_data = []
album_caption = []
@dp.message_handler(content_types = ['photo'])
async def on_photo_message(message: types.Message):
    
    for admin in admins:
        if admin == message.from_user.id:
            if message.media_group_id:
                album_data.append(message.photo[-1].file_id)
                if message.caption:
                    album_caption.append(message.caption)
                else:
                    album_caption.append('')
                await message.reply('<b>{}</b> - foto yuklandi'.format(len(album_data)))
                break
            else:
                user = await get_user()
                for chat_id in user.fetchall():
                    await bot.send_photo(chat_id[1], photo = message.photo[-1].file_id, caption = message.caption,caption_entities=message.caption_entities)
           
            
# @dp.callback_query_handler()
# async def on_callback_query(callback_query: types.CallbackQuery):
#     if callback_query.data=='1':
#         await callback_query.answer('Kanalga obuna buling',show_alert=True)
    
    
@dp.message_handler(content_types = ["new_chat_members"])
async def on_new_chat_member(message: types.Message):
    await message.delete() 
    await message.answer('<b>{}</b> - Guruhga hush kelibsiz😊'.format(message.from_user.full_name))
       
@dp.message_handler(content_types = ["left_chat_member"])
async def on_left_chat_member(message: types.Message):
    await message.delete()

@dp.message_handler(content_types = ["new_chat_title"])
async def on_new_chat_title(message: types.Message):
    await message.delete()
    print(message.new_chat_title)

@dp.message_handler(content_types = ["new_chat_photo"])
async def on_new_chat_photo(message: types.Message):
    await message.delete()
    print(message.new_chat_photo)

@dp.message_handler(content_types = ["delete_chat_photo"])
async def on_delete_chat_photo(message: types.Message):
    await message.delete()
    print(message.delete_chat_photo)
    
# pin
# @dp.message_handler(content_types=["new_chat_pinned_message"])
# async def on_new_chat_pinned_message(message: types.Message):
#     await message.delete()

@dp.message_handler(content_types = ["pinned_message"])
async def on_pinned_message(message: types.Message):
    await message.delete()
    print(message.pinned_message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    conn.close()