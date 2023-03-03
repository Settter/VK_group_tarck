import time

import telebot

bot = telebot.TeleBot('5266363672:AAEyg1z8QrEwfS31bJUhGybWZs7zpveD7wY')


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = str(message.from_user.id)
    if open('bot_save_id_YoN.txt', 'r').read().find('1') != -1:
        ids = open('bot_user_id.txt', 'r').read()
        if ids.find(user_id) == -1:
            bot.send_message(message.chat.id,'Добрый день ' + message.from_user.first_name + ", вы подписались на уведомления об обновлениях в группах.")
            with open('bot_user_id.txt', 'w') as file:
                file.write(ids + user_id + ' ')
    pass


def mass_message(keyword, group_link, group_id, post_id):
    ids = open('bot_user_id.txt', 'r').read().split(' ')
    for i in range(len(ids)):
        if ids[i] != '':
            bot.send_message(int(ids[i]),
                             'В группе ' + group_link + ' вышел пост с ключевым словом ' + keyword + ' - ' + group_link + '?w=wall-' + str(
                                 group_id) + '_' + str(post_id))


def bot_main():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)


