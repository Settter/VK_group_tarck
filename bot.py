import time

import telebot

bot = telebot.TeleBot('5266363672:AAEyg1z8QrEwfS31bJUhGybWZs7zpveD7wY')


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = str(message.from_user.id)
    if open('configuration_files/save_id_rule.txt', 'r').read().find('1') != -1:
        ids = open('service_files/user_id_file.txt', 'r').read()
        if ids.find(user_id) == -1:
            bot.send_message(message.chat.id,'Добрый день ' + message.from_user.first_name + ", вы подписались на уведомления об обновлениях в группах.")
            with open('service_files/user_id_file.txt', 'w') as file:
                file.write(ids + user_id + ' ')
    pass


def mass_message(keyword, group_link, group_id, post_id):
    ids = open('service_files/user_id_file.txt', 'r').read().split(' ')
    for i in range(len(ids)):
        if ids[i] != '':
            bot.send_message(int(ids[i]),
                             'В группе ' + group_link + ' вышел подходящий пост - https://vk.com/' + group_link + '?w=wall-' + str(
                                 group_id) + '_' + str(post_id))


def bot_main():
    try:
        bot.delete_webhook()
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)



