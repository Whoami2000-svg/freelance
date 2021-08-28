import telebot
from telebot import types
import requests
import time 
import json

TOKEN = 'Bearer 58d9c04ba56ea1e36baedc47f6db31a0f5dd0bfa'
ADMIN = 566266388
TELEBOT_TOKEN = '1689331285:AAGOQeZ_UjZ6zZXEqHZj9RfxI0PzUVcilbI'


bot = telebot.TeleBot(TELEBOT_TOKEN)
last_offers = []
PARSING = [1]



def get_new_offers():
    url = "https://api.freelancehunt.com/v2/projects?filter[only_my_skills]=2"
    payload={}
    headers = {
      'Authorization': TOKEN
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    responce = response.json().get('data')
    offers = []
    for i in responce:
        if not i.get('id') in last_offers:
            if len(last_offers) == 10:
                last_offers.pop(0)
            last_offers.append(i.get('id'))
            offers.append(i)
    return offers


@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id == ADMIN:
        while True:
            new_offers = get_new_offers()
            for i in new_offers:
                link = i.get("links").get("self").get("web")
                i = i.get("attributes")
                name = i.get("name")
                description = i.get("description")
                cost = i.get("budget")
                if cost == None:
                    cost = 'не указан'
                else:
                    cost = str(cost.get("amount")) + cost.get("currency") 
                text = 'Название проекта:    ' + name + '\n\nОписание проекта:    ' + description + '\n\nБюджет проекта:    ' + cost + '\n' + link

                try:
                    bot.send_message(message.chat.id, text)
                except:
                    text = 'Название проекта:    ' + name + '\n\nОписание проекта:    ' + 'слишком длинное' + '\n\nБюджет проекта:    ' + cost + '\n' + link
                    bot.send_message(message.chat.id, text)
                time.sleep(20)
            time.sleep(300)
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Так бы и сказал') 
        bot.send_message(message.chat.id, 'Точно, канай! И пусть канает отсюда, а то я ему рога поотшибаю, пасть порву, моргалы выколю! ВСЮ ЖИЗНЬ РАБОТАТЬ НА ЛЕКАРСТВА БУДЕШЬ! Сарделька, сосиска, редиска, Навуходоносор, петух гамбургский!!!', reply_markup=keyboard)



if __name__ == '__main__':
    bot.infinity_polling()