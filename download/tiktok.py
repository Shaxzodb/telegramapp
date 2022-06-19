import logging
import requests
# Tiktok video yuklash
async def tiktok(message,HOST,KEY,URL):
    
    try:
        url = URL
        querystring = {"url":f"{message.text}"}

        headers = {
            "X-RapidAPI-Key": KEY,
	        "X-RapidAPI-Host": HOST
	        
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        await message.answer_video(video = response.json()['itemData']['video']['no_watermark']['hd']['url'])
    except Exception as error:
        
        #await message.answer('<b>{}</b> - tiktok video yuklanmadi qaytib link ni tug\'riligini tekshirib ko\'ring'.format(message.text))
        await message.answer('<b>{}</b> - tiktok video tehnik sabablarga kura yuklanmadi buning uchun uzur suraymiz, botda tuzatish ishlari olib borilyapti tez orada bu xato tuzatiladi'.format(message.text))
        logging.error(f'Tiktok File: {error}')

    