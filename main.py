import telebot
import os
import requests
from datetime import datetime
import pytz
import json

from keep_alive import keep_alive
keep_alive()

bot = telebot.TeleBot(token=os.environ.get('7116309895:AAFnL31sadM5C0mOgAI1Zy9RBw2zFjl5eOw'))
def timestamp(timestamp):
    dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    local_time = dt.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%d %b %y %I:%M %p')
    return local_time

def get_data(UID):
    headers = {
    'authority': 'ff-info.vercel.app',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'origin': 'https://jinix6.github.io',
    'referer': 'https://jinix6.github.io/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
}
    params = {
    'uid': UID,
}
    response = requests.get('https://ff-info.vercel.app/', params=params, headers=headers)
    return response.text

@bot.message_handler(func=lambda message: True)
def echo_all(message):


    data = get_data(message.text)
    data_dict = json.loads(data)
    message_text = f"""
𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗜𝗡𝗙𝗢
├─Nᴀᴍᴇ: `{data_dict["Nickname"]}`
├─Uɪᴅ: `{data_dict["AccountUID"]}`
├─Lᴠ: {data_dict["Level"]} 
│    └─Exᴘ: {data_dict["Exp"]}
├─Rᴇɢɪᴏɴ: {data_dict["Region"]}
├─Lɪᴋᴇ: {data_dict["Like"]}
├─Bᴀɴɴᴇʀ Iᴅ: `{data_dict["BannerID"]}`
├─Aᴠᴀᴛᴀʀ Iᴅ: `{data_dict["AvatarID"]}`
├─Bɪᴏ: `{data_dict["Bio"]}`
├─𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗔𝗖𝗧𝗜𝗩𝗜𝗧𝗬
│  ├─Bʀ Rᴀɴᴋ: {data_dict["BrPoint"]} ({data_dict["BrScore"]})
│  ├─Lᴀsᴛ Lᴏɢɪɴ: {timestamp(int(data_dict["LastLogin"]))}
│  └─Cʀᴇᴀᴛᴇᴅ Aᴛ: {timestamp(int(data_dict["AccountCreated"]))}
└─𝗚𝗨𝗜𝗟𝗗 𝗜𝗡𝗙𝗢
          ├─Nᴀᴍᴇ: `{data_dict["GuildName"]}`
          ├─Iᴅ: `{data_dict["GuildID"]}`
          └─*Leader Info*
                     ├─Nᴀᴍᴇ: `{data_dict["GuildLeaderNickName"]}`
                     ├─Uɪᴅ: `{data_dict["GuildLeaderUid"]}`
                     └─Lᴠ: {data_dict["GuildLeaderLvl"]} 
                             └─Exᴘ: {data_dict["GuildLeaderExp"]}
"""
    
    PROFILE_URL = data_dict["ProfileUrl"]
    bot.send_photo(message.chat.id, PROFILE_URL, caption=message_text, reply_to_message_id=message.message_id, parse_mode="Markdown")

if __name__ == '__main__':
    bot.polling()
