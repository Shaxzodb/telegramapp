from sqlite3 import connect
#__all__ = ['get_user','count_user','add_user','conn','cursor']
aSSA="SASA"
conn=connect("sqlite3.conn")
cursor=conn.cursor()
try:
    table ="""CREATE TABLE users("id" INTEGER,chat_id INTEGER ,last_name VARCHAR(255), first_name VARCHAR(255),PRIMARY KEY("id" AUTOINCREMENT));"""
    cursor.execute(table)
    conn.commit()
    print('Table is created')
except:
    print("Table already exists")
    
async def add_user(message):
    try:
        user=cursor.execute('''SELECT * FROM users WHERE chat_id=? Limit 1''',(message.chat.id,))
        
        if not user.fetchone():
            print("User is already registered")
            cursor.execute(f"INSERT INTO users(chat_id, last_name,first_name) VALUES ({message.chat.id}, '{message.from_user.last_name}', '{message.from_user.first_name}')")
            conn.commit()
            await message.answer('Salom <b>{}</b>! - botga hush kelibsiz bot haqida malumot olish uchun /help buyrug\'ini kiriting 😊'.format(message.from_user.full_name))
        else:
            # cursor.execute(f"UPDATE users SET last_name={message.from_user.last_name}, first_name={message.from_user.first_name} WHERE chat_id={message.chat.id}")
            # conn.commit()
            await message.answer('Salom <b>{}</b>! - botga qaytganingizdan hursandmiz 😊'.format(message.from_user.full_name))
            

            
    except Exception as err:
        print('Error: ',err)
async def get_user():
    try:
        user= cursor.execute('''SELECT * FROM users''')
        return user
    except Exception as err:
        print('Error: ',err)
        
async def count_user():
    try:
        user = cursor.execute('''SELECT COUNT(chat_id) FROM users''')
        return user.fetchone()[0]

    except Exception as err:
        print('Error: ',err)


if __name__ == '__main__':
    conn.close()