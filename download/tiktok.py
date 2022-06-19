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
        await message.answer_video(video = response.json()['itemData']['video']['dynamic_cover']['url_list'][0])
    except Exception as error:
        
        await message.answer('<b>{}</b> - tiktok video yuklanmadi qaytib link ni tug\'riligini tekshirib ko\'ring'.format(message.text))
        logging.error(f'Tiktok File: {error}')

    