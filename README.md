# Telegram Bot Python Aiogram

```cmd
pipenv install 
```
## Run Bot
#
> ` make `  or  ` python bot.py `
#
#### TikTok Download
```python
import requests
# Tiktok video yuklash
async def tiktok(message,HOST,KEY,URL):
    
    try:
        url = URL

        querystring = {"url":f"{message.text}","hd":"0"}

        headers = {
	        "X-RapidAPI-Host": HOST,
	        "X-RapidAPI-Key": KEY
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        await message.answer_video(video = response.json()['data']['play'])
    except:
        await message.answer('<b>{}</b> - tiktok video yuklanmadi qaytib link ni tug\'riligini tekshirib ko\'ring'.format(message.text))
       

    
```
##
#### Instagram Download
```python

import requests
# Instagram video yuklash
async def instagram(message,HOST,KEY,URL):
    try:
        url = URL

        querystring = {"url":f"{message.text}"}

        headers = {
	        "X-RapidAPI-Host": HOST,
	        "X-RapidAPI-Key": KEY
        }
        response = requests.request("GET", url, headers = headers, params = querystring)
        if type(response.json()["media"]) != list:
            
            await message.answer_photo(photo = response.json()["media"])
            await message.answer_video(video = response.json()["media"])
        else:
            for img in list(response.json()["media"]):
            
                await message.answer_photo(photo = img )
                await message.answer_video(video = img )
    except:
        await message.answer('<b>{}</b> - tiktok video yuklanmadi qaytib link ni tug\'riligini tekshirib ko\'ring'.format(message.text))
   
```
> Telegram Bot pacages

- python version 3.10.x
    - aiogram
    - pysqlite3
    - requests
    # telegramapp
# telegramapp
# telegramapp
