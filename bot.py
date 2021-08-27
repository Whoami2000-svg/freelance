import telebot
import requests
import time 
import json

TOKEN = 'Bearer 58d9c04ba56ea1e36baedc47f6db31a0f5dd0bfa'
ADMIN = 566266388
TELEBOT_TOKEN = '1689331285:AAGOQeZ_UjZ6zZXEqHZj9RfxI0PzUVcilbI'



bot = telebot.TeleBot(TELEBOT_TOKEN)



last_offers = []
offers_for_kill = []
new_bid = []


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

def get_new_messages():
    url = "https://api.freelancehunt.com/v2/threads"
    payload={}
    headers = {
      'Authorization': TOKEN
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    responce = response.json().get('data')
    for i in responce:
        if (i.get('attributes').get("is_unread")):
            return True 
    return False

def get_all_bids(url):
    payload={}
    headers = {
      'Authorization': TOKEN
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    responce = response.json().get('data')
    return responce

@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id == ADMIN:
        bot.send_message(message.chat.id, 'С возвращением, босс.\n/parser - режим парсинга;\n/kill - режим "мгновенное убийство".')
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Так бы и сказал') 
        bot.send_message(message.chat.id, 'Точно, канай! И пусть канает отсюда, а то я ему рога поотшибаю, пасть порву, моргалы выколю! ВСЮ ЖИЗНЬ РАБОТАТЬ НА ЛЕКАРСТВА БУДЕШЬ! Сарделька, сосиска, редиска, Навуходоносор, петух гамбургский!!!', reply_markup=keyboard)

@bot.message_handler(commands=["parser"])
def parser(message):
    if message.chat.id == ADMIN:
        bot.send_message(message.chat.id, 'Активирован режим парсинга\n/kill - режим "мгновенное убийство".')
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
                bot.send_message(message.chat.id, text)
            time.sleep(300) #ИСПРАВИТЬ
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Так бы и сказал') 
        bot.send_message(message.chat.id, 'Точно, канай! И пусть канает отсюда, а то я ему рога поотшибаю, пасть порву, моргалы выколю! ВСЮ ЖИЗНЬ РАБОТАТЬ НА ЛЕКАРСТВА БУДЕШЬ! Сарделька, сосиска, редиска, Навуходоносор, петух гамбургский!!!', reply_markup=keyboard)



@bot.message_handler(commands=["kill"])
def kill(message):
    if message.chat.id == ADMIN:
        bot.send_message(message.chat.id, 'Активирован режим "мгновенное убийство"\n/parser - режим парсинга.')
        while len(get_new_offers()) == 0:
                time.sleep(300)
        new_offers = get_new_offers()
        for i in new_offers:
            offers_for_kill.append(i)
        i = offers_for_kill[0]
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
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Оставить ставку', 'Проигнорировать') 
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
        bot.register_next_step_handler(message, kill_message)   
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Так бы и сказал') 
        bot.send_message(message.chat.id, 'Точно, канай! И пусть канает отсюда, а то я ему рога поотшибаю, пасть порву, моргалы выколю! ВСЮ ЖИЗНЬ РАБОТАТЬ НА ЛЕКАРСТВА БУДЕШЬ! Сарделька, сосиска, редиска, Навуходоносор, петух гамбургский!!!', reply_markup=keyboard)


def kill_message(message):
    if message.text == 'Оставить ставку':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Отмена')
        bot.send_message(message.chat.id, 'Сколько дней возмёте на заказ?', reply_markup=keyboard)
        bot.register_next_step_handler(message, bid_days)
    else:
        offers_for_kill.pop(0)
        if len(offers_for_kill) > 0:
            i = offers_for_kill[0]
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
            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Оставить ставку', 'Проигнорировать') 
            bot.send_message(message.chat.id, text, reply_markup=keyboard)
            bot.register_next_step_handler(message, kill_message)
        else:
            while len(get_new_offers()) == 0:
                time.sleep(300)
            new_offers = get_new_offers()
            for i in new_offers:
                offers_for_kill.append(i)
            i = offers_for_kill[0]
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
            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Оставить ставку', 'Проигнорировать') 
            bot.send_message(message.chat.id, text, reply_markup=keyboard)
            bot.register_next_step_handler(message, kill_message)    


def bid_days(message):
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Вы отменили ставку')
        i = offers_for_kill[0]
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
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Оставить ставку', 'Проигнорировать') 
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
        bot.register_next_step_handler(message, kill_message)
    else:
        try:
            days = int(message.text)
            new_bid.append(str(days))
            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Отмена')
            bot.send_message(message.chat.id, 'Напишите комментарий', reply_markup=keyboard)
            bot.register_next_step_handler(message, bid_comment)
        except:
            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Отмена')
            bot.send_message(message.chat.id, 'Ошибка. Укажите ещё раз!', reply_markup=keyboard)
            bot.register_next_step_handler(message, bid_days)


def bid_comment(message):
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Вы отменили ставку')
        i = offers_for_kill[0]
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
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Оставить ставку', 'Проигнорировать') 
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
        bot.register_next_step_handler(message, kill_message)
    else:
        new_bid.append(message.text)
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row(' << ', 'Отмена')
        i = offers_for_kill[0]
        link = i.get("links").get("bids")
        responce = get_all_bids(link)
        currency = 0
        for i in responce:
            if not i.get("attributes").get("is_hidden"):
                currency = i.get("attributes").get("budget").get("currency")
                new_bid.append(currency)
                bot.send_message(message.chat.id, 'Теперь укажите сумму, за которую будете батрачить) (в ' + currency + ')', reply_markup=keyboard)
                bot.register_next_step_handler(message, bid_cost)
                break
        while currency == 0:
            time.sleep(300)
            responce = get_all_bids(link)
            currency = 0
            for i in responce:
                if not i.get("attributes").get("is_hidden"):
                    currency = i.get("attributes").get("budget").get("currency")
                    new_bid.append(currency)
                    bot.send_message(message.chat.id, 'Теперь укажите сумму, за которую будете батрачить) (в ' + currency + ')', reply_markup=keyboard)
                    bot.register_next_step_handler(message, bid_cost)
                    break






def bid_cost(message):
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Вы отменили ставку')
        i = offers_for_kill[0]
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
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Оставить ставку', 'Проигнорировать') 
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
        bot.register_next_step_handler(message, kill_message)
    elif message.text == ' << ':
        new_bid.pop(1)
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Отмена')
        bot.send_message(message.chat.id, 'Напишите комментарий заново.', reply_markup=keyboard)
        bot.register_next_step_handler(message, bid_comment)
    else:
        try:
            cost = int(message.text)
            new_bid.append(str(cost))
            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Подтвердить', 'Отмена')
            bot.send_message(message.chat.id, 'Ставка сформированна. Опубликовать?', reply_markup=keyboard)
            bot.register_next_step_handler(message, bid_publication)
        except:
            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row(' << ', 'Отмена')
            bot.send_message(message.chat.id, 'Ошибка. Укажите ещё раз!', reply_markup=keyboard)
            bot.register_next_step_handler(message, bid_cost)


def bid_publication(message):
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Вы отменили ставку')
        i = offers_for_kill[0]
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
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Оставить ставку', 'Проигнорировать') 
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
        bot.register_next_step_handler(message, kill_message)
    else:
        i = offers_for_kill[0]
        link = i.get("links").get("bids")
        payload = json.dumps({
          "days": new_bid[0],
          "safe_type": "employer",
          "budget": {
            "amount": new_bid[3],
            "currency": new_bid[2]
          },
          "comment": new_bid[1],
          "is_hidden": True
        })
        headers = {
          'Authorization': TOKEN,
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", link, headers=headers, data=payload)
        offers_for_kill.pop(0)
        new_bid.clear()
        bot.send_message(message.chat.id, 'Ставка опубликована.')
        if len(offers_for_kill) > 0:
            i = offers_for_kill[0]
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
            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Оставить ставку', 'Проигнорировать') 
            bot.send_message(message.chat.id, text, reply_markup=keyboard)
            bot.register_next_step_handler(message, kill_message)
        else:
            while len(get_new_offers()) == 0:
                    time.sleep(300)
            new_offers = get_new_offers()
            for i in new_offers:
                offers_for_kill.append(i)
            i = offers_for_kill[0]
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
            keyboard = telebot.types.ReplyKeyboardMarkup()
            keyboard.row('Оставить ставку', 'Проигнорировать') 
            bot.send_message(message.chat.id, text, reply_markup=keyboard)
            bot.register_next_step_handler(message, kill_message)
                
if __name__ == '__main__':
    bot.infinity_polling()

