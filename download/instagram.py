import logging
import requests
# Instagram video yuklash
async def instagram(message,HOST,KEY,URL):
    try:
        url = URL
        # BU UZGARDI
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
    except Exception as error:
        await message.answer('<b>{}</b> - instagram video yuklanmadi qaytib link ni tug\'riligini tekshirib ko\'ring'.format(message.text))
        logging.error(f'Instagram File: {error}')
