import json
import subprocess
import re
from google.protobuf import json_format
import os
from Crypto.Cipher import AES
import base64
import binascii
import requests
import importlib.util
import telebot
import requests
import json
from datetime import datetime
import pytz
import time
import sample_pb2
from keep_alive import keep_alive
from telebot import types, ExceptionHandler
keep_alive()


class MyExceptionHandler(ExceptionHandler):
    async def handle(self, exception):
        print(exception)
        

def timestamp(timestamp):
    timezone_str = 'Asia/Kolkata'  # GMT+05:30
    local_timezone = pytz.timezone(timezone_str)
    dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    local_time = dt.astimezone(local_timezone)
    formatted_time = local_time.strftime('%d %b %y %I:%M %p')
    return formatted_time


TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN, exception_handler=MyExceptionHandler())



def get_data(text):
    data = re.sub(r'"([^"]*?)"', lambda x: x.group(0).replace('\n', r'\\n'), text)
    def extract(pattern, data):
        match = re.search(pattern, data)
        return match.group(1) if match else None
    uid = extract(r'\[\d+\]  1,1 -> <int> = (\d+)', data)
    nickname = extract(r'\[\d+\]  1,3 -> <string> = "(.*?)"', data)
    region = extract(r'\[\d+\]  1,5 -> <string> = "(.*?)"', data)
    bio = extract(r'\[\d+\]  9,9 -> <string> = "(.*?)"', data)
    lvl = extract(r'\[\d+\]  1,6 -> <int> = (\d+)', data)
    exp = extract(r'\[\d+\]  1,7 -> <int> = (\d+)', data)
    guild_id = extract(r'\[\d+\]  6,1 -> <int> = (\d+)', data)
    banner = extract(r'\[\d+\]  1,11 -> <int> = (\d+)', data)
    avatar = extract(r'\[\d+\]  1,12 -> <int> = (\d+)', data)
    br_point = extract(r'\[\d+\]  1,15 -> <int> = (\d+)', data)
    br_score = extract(r'\[\d+\]  1,39 -> <int> = (\d+)', data)
    like = extract(r'\[\d+\]  1,21 -> <int> = (\d+)', data)
    id_created = extract(r'\[\d+\]  1,44 -> <int> = (\d+)', data)
    last_login = extract(r'\[\d+\]  1,24 -> <int> = (\d+)', data)
    guild_leader_uid = extract(r'\[\d+\]  6,3 -> <int> = (\d+)', data)
    guild_leader_lvl = extract(r'\[\d+\]  7,6 -> <int> = (\d+)', data)
    guild_leader_exp = extract(r'\[\d+\]  7,7 -> <int> = (\d+)', data)
    profile_url = extract(r'\[\d+\]  1,49,1 -> <string> = "(.*?)"', data)
    guild_name = extract(r'\[\d+\]  6,2 -> <string> = "(.*?)"', data)
    guild_leader_name = extract(r'\[\d+\]  7,3 -> <string> = "(.*?)"', data)
    return uid, nickname, region, lvl, exp, banner, avatar, like, guild_id, profile_url, guild_name, br_point, br_score, guild_leader_name, guild_leader_uid, guild_leader_lvl, bio, guild_leader_exp, id_created, last_login









def checkUID(UID):
    url = "https://shop.garena.sg/api/auth/player_id_login"
    payload = json.dumps({
      "app_id": 100067,
      "login_id": UID,
      "app_server_id": 0
    })
    headers = {
      'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
      'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
      'x-datadome-clientid': "fsXouxJd1lCWuCZxsmB~2nQBZ0oP5vyvlx5fkvVNQELslEQcGZcmxZmu74bkdA8pIFNf2GPw1pf10ruR9N2TLVOFY~IRo2cB3sxfh2yGiUDmPXFjkZDGw1a0iG5~ntYc"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.text

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def GetData(UID, Fetch_url):
    def aes_cbc_encrypt(key, iv, plaintext):
        aes = AES.new(base64.b64decode(key), AES.MODE_CBC, base64.b64decode(iv))
        padded_plaintext = pad(plaintext)
        ciphertext = aes.encrypt(padded_plaintext)
        return binascii.hexlify(ciphertext).decode()

    def pad(text):
        padding_length = AES.block_size - (len(text) % AES.block_size)
        padding = bytes([padding_length] * padding_length)
        return text + padding

    def to_uint8_array(hex_string):
        return bytes.fromhex(re.sub(r'\W+', '', hex_string))

    def from_uint8_array(byte_array):
        return ' '.join(format(byte, '02X') for byte in byte_array)

    def encode(decoded):
        encoded = ""
        try:
            if not decoded:
                return encoded
            test1_message = sample_pb2.Test1()
            payload = json.loads(decoded)
            json_format.ParseDict(payload, test1_message)
            encoded = '<' + from_uint8_array(test1_message.SerializeToString()) + '>'
        except Exception as e:
            encoded = "Error:\n" + str(e)
            print(e)
        return encoded
    
    example_json = f"""{{
     "a": {UID},
     "b": 7
    }}"""

    encoded_result = encode(example_json)
    normal_text = encoded_result.replace("<", "").replace(">", "").replace(" ", "")
    key = os.environ.get('KEY')
    iv = os.environ.get('IV')
    plaintext = binascii.unhexlify(normal_text)
    encrypted_text = aes_cbc_encrypt(key, iv, plaintext)
    
    url = Fetch_url
    payload = bytes.fromhex(encrypted_text)
    headers = {
      'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 13; A063 Build/TKQ1.221220.001)",
      'Connection': "Keep-Alive",
      'Accept-Encoding': "gzip",
      'Content-Type': "application/octet-stream",
      'Expect': "100-continue",
      'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInN2ciI6IjMiLCJ0eXAiOiJKV1QifQ.eyJhY2NvdW50X2lkIjo4ODMxMzUxNTU2LCJuaWNrbmFtZSI6IktleTNFMXIyUCIsIm5vdGlfcmVnaW9uIjoiSU5EIiwibG9ja19yZWdpb24iOiJJTkQiLCJleHRlcm5hbF9pZCI6IjgxY2JjNWQxOWIzZThjOGI4MjQ5MjYzZDhhN2U5OTk5IiwiZXh0ZXJuYWxfdHlwZSI6NCwicGxhdF9pZCI6MSwiY2xpZW50X3ZlcnNpb24iOiIxLjEwMy43IiwiZW11bGF0b3Jfc2NvcmUiOjAsImlzX2VtdWxhdG9yIjpmYWxzZSwiY291bnRyeV9jb2RlIjoiSU4iLCJleHRlcm5hbF91aWQiOjMwODU3MzE2MDYsInJlZ19hdmF0YXIiOjEwMjAwMDAwNSwic291cmNlIjowLCJsb2NrX3JlZ2lvbl90aW1lIjoxNzA3MTk5MDE5LCJjbGllbnRfdHlwZSI6Miwic2lnbmF0dXJlX21kNSI6Ijc0MjhiMjUzZGVmYzE2NDAxOGM2MDRhMWViYmZlYmRmIiwidXNpbmdfdmVyc2lvbiI6MSwicmVsZWFzZV9jaGFubmVsIjoiYW5kcm9pZCIsInJlbGVhc2VfdmVyc2lvbiI6Ik9CNDMiLCJleHAiOjE3MDc1MzI0NDB9.1nNG0FbjtuIZnUg1sZXn_p5N6OjJG29sP2m4Rt5HVK8",
      'X-Unity-Version': "2018.4.11f1",
      'X-GA': "v1 1",
      'ReleaseVersion': "OB43"
    }
    response = requests.post(url, data=payload, headers=headers)
    
    with open("c.bin", "wb") as file:
        file.write(response.content)
    command = f"protodeep c.bin -t protobuf > output.txt"
    output = run_command(command)
    #os.remove("c.bin")
    
    with open("output.txt", "r") as file:
        output_contents = file.read()
        #os.remove("output.txt")
    return output_contents


#data = GetData("1633864660", "https://client.ind.freefiremobile.com/GetWorkshopAuthorInfo")
#print(data)




@bot.message_handler(func=lambda message: True)
def handle_sticker(message):
    try:
        check = checkUID(message.text)
        if not "error" in check:
            data = GetData(message.text, "https://client.ind.freefiremobile.com/GetPlayerPersonalShow")
            uid, nickname, region, lvl, exp, banner, avatar, like, guild_id, profile_url, guild_name, br_point, br_score, guild_leader_name, guild_leader_uid, guild_leader_lvl, bio, guild_leader_exp, id_created, last_login = get_data(data)
            
            
            data = GetData(message.text, "https://client.ind.freefiremobile.com/GetWorkshopAuthorInfo")
            matches = re.findall(r'"([^"]{36})"', data)
            result_str = ""
            for i, match in enumerate(matches, start=1):
                result_str += f"```{i}\n#FREEFIRE{match}```\n"
            message_text = f"""
𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗜𝗡𝗙𝗢
├─Nᴀᴍᴇ: `{nickname}`
├─Uɪᴅ: `{uid}`
├─Lᴠ: {lvl} 
│    └─Exᴘ: {exp}
├─Rᴇɢɪᴏɴ: {region}
├─Lɪᴋᴇ: {like}
├─Bᴀɴɴᴇʀ Iᴅ: `{banner}`
├─Aᴠᴀᴛᴀʀ Iᴅ: `{avatar}`
├─Bɪᴏ: `{bio}`
├─𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗔𝗖𝗧𝗜𝗩𝗜𝗧𝗬
│  ├─Bʀ Rᴀɴᴋ: {br_point} ({br_score})
│  ├─Lᴀsᴛ Lᴏɢɪɴ: {timestamp(int(last_login))}
│  └─Cʀᴇᴀᴛᴇᴅ Aᴛ: {timestamp(int(id_created))}
├─𝗚𝗨𝗜𝗟𝗗 𝗜𝗡𝗙𝗢
│          ├─Nᴀᴍᴇ: `{guild_name}`
│          ├─Iᴅ: `{guild_id}`
│          └─*Leader Info*
│                     ├─Nᴀᴍᴇ: `{guild_leader_name}`
│                     ├─Uɪᴅ: `{guild_leader_uid}`
│                     └─Lᴠ: {guild_leader_lvl} 
│                             └─Exᴘ: {guild_leader_exp}
𝗖𝗥𝗔𝗙𝗧𝗟𝗔𝗡𝗗
{result_str}
"""
       
            bot.send_chat_action(message.chat.id, 'typing')
            if profile_url != None:
                bot.send_photo(message.chat.id, profile_url, caption=message_text, reply_to_message_id=message.message_id, parse_mode="Markdown")
            else:
                bot.reply_to(message, message_text, parse_mode="Markdown")
            

    except Exception as e:
        print(e)



@bot.message_handler(commands=['cancel', 'start'])
def start_fun(message):
    message_text = "🤖"
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, message_text, parse_mode="Markdown")



bot.polling(none_stop=True)
