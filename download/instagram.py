import requests

async def instagram(message,HOST,KEY,URL):
    try:
        url = URL

        querystring = {"url":f"{message.text}"}

        headers = {
	        "X-RapidAPI-Host": HOST,
	        "X-RapidAPI-Key": KEY
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        if type(response.json()["media"])!=list:
            
            await message.answer_photo(photo = response.json()["media"])
            await message.answer_video(video = response.json()["media"])
        else:
            for i in list(response.json()["media"]):
            
                await message.answer_photo(photo =i )
                await message.answer_video(video = i)
    except:
        await message.answer('<b>{}</b> - tiktok video yuklanmadi qaytib link ni tug\'riligini tekshirib ko\'ring'.format(message.text))
   
