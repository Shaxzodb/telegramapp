from sqlite3 import connect



db=connect("sqlite3.db")
cursor=db.cursor()

try:
    table ="""CREATE TABLE users("id" INTEGER,chat_id INTEGER ,last_name VARCHAR(255), first_name VARCHAR(255),PRIMARY KEY("id" AUTOINCREMENT));"""
    cursor.execute(table)
    db.commit()
    print('Table is created')
except:
    print("Table already exists")
    
async def add_user(message):
    try:
        user=cursor.execute('''SELECT * FROM users WHERE chat_id=? Limit 1''',(message.chat.id,))
        
        if not user.fetchone():
            print("User is already registered")
            cursor.execute(f"INSERT INTO users(chat_id, last_name,first_name) VALUES ({message.chat.id}, '{message.from_user.last_name}', '{message.from_user.first_name}')")
            db.commit()
            await message.answer('Salom <b>{}</b>! - botga hush kelibsiz bot haqida malumot olish uchun /help buyrug\'ini kiriting 😊'.format(message.from_user.full_name))
        else:
            await message.answer('Salom <b>{}</b>! - botga qaytganingizdan hursandmiz 😊'.format(message.from_user.full_name))
            

            
    except Exception as err:
        print('Error: ',err)
async def get_user():
    try:
        user=cursor.execute('''SELECT * FROM users''')
        return user
    except Exception as err:
        print('Error: ',err)

    
