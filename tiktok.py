import requests

async def tiktok(message,HOST,KEY):
    
    try:
        url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

        querystring = {"url":f"{message.text}","hd":"0"}

        headers = {
	        "X-RapidAPI-Host": HOST,
	        "X-RapidAPI-Key": KEY
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        await message.answer_video(video = response.json()['data']['play'])
    except:
        await message.answer('<b>{}</b> - tiktok video yuklanmadi qaytib link ni tug\'riligini tekshirib ko\'ring'.format(message.text))
       

    