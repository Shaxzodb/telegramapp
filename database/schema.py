from sqlite3 import connect

from bot import logging
import datetime
import asyncio
__all__ = ['get_user','count_user','add_user','conn']

conn=connect("sqlite3.db")
cursor=conn.cursor()
try:
    table ="""CREATE TABLE users("id" INTEGER,chat_id INTEGER ,last_name VARCHAR(255), first_name VARCHAR(255),PRIMARY KEY("id" AUTOINCREMENT));"""
    cursor.execute(table)
    conn.commit()
    logging.info("Database is created")
except:
    logging.info("Database is already created")
    pass
    
async def add_user(message):
    try:
        user=cursor.execute('''SELECT * FROM users WHERE chat_id=? Limit 1''',(message.chat.id,))
        
        if not user.fetchone():
            print("User is already registered")
            cursor.execute(f"INSERT INTO users(chat_id, last_name,first_name) VALUES ({message.chat.id}, '{message.from_user.last_name}', '{message.from_user.first_name}')")
            conn.commit()
            await message.answer('Salom <b>{}</b>! - botga hush kelibsiz bot haqida malumot olish uchun /help buyrug\'ini kiriting 😊'.format(message.from_user.full_name))
        else:
            cursor.execute(f"UPDATE users SET last_name = '{message.from_user.last_name}', first_name = '{message.from_user.first_name}' WHERE chat_id = {message.chat.id}")
            conn.commit()
            await message.answer('Salom <b>{}</b>! - botga qaytganingizdan hursandmiz 😊'.format(message.from_user.full_name))
            

            
    except Exception as error:
        logging.error(f'Database: {error}')
async def get_user():
    try:
        user= cursor.execute('''SELECT * FROM users''')
        return user
    except Exception as error:
        logging.error(f'Database: {error}')
        
async def count_user():
    try:
        user = cursor.execute('''SELECT COUNT(chat_id) FROM users''')
        return user.fetchone()[0]

    except Exception as error:
        logging.error(f'Database: {error}')

def Copy_DataBase():
    try:
        cursor.execute('''CREATE TABLE users_copy("id" INTEGER,chat_id INTEGER ,last_name VARCHAR(255), first_name VARCHAR(255));''')
        cursor.execute("INSERT INTO users_copy SELECT * FROM users;")
        conn.commit()
    except Exception as error:
        logging.error(f'Database: {error}')

if datetime.date.today().day == 24:
    try:
        cursor.execute("DROP TABLE users_copy;")
        conn.commit()
    except Exception as warning:
        #logging.warning(f'Database: {warning}')
        print('Log: ',warning)
    Copy_DataBase()

if __name__ == '__main__':
    conn.close()