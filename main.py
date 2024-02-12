import telebot
import os
import requests
from keep_alive import keep_alive
keep_alive()


bot = telebot.TeleBot(token=os.environ.get('token'))

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
    return response.content

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    data = get_data(message.text)
    message_text = f"```json\n{data}```"
    bot.reply_to(message, message_text, parse_mode="Markdown")

if __name__ == '__main__':
    bot.polling()