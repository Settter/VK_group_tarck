import re
import time
from threading import Thread

import requests

from bot import mass_message, bot_main


def get_post_link(_id, _domain, offset, count):
    # без offset выведет закрем, если он есть, а с offset выведет пост исключая закреп (offset обозначает с какого
    # поста начать)
    immutable_link = 'https://api.vk.com/method/'
    method = 'wall.get'
    for_who = 'all'
    access_token = '50934c3550934c3550934c354550e8167b5509350934c353283b43e2d4451cd19e0fafb'
    version = '5.131'
    return immutable_link + method + "?owner_id=" + _id + '&domain=' + _domain + '&offset=' + offset + '&count=' + count + '&filter=' + for_who + '&access_token=' + access_token + '&v=' + version


def get_first_post(owner_, domain_, offset='0'):
    posts = requests.get(
        get_post_link(_id=owner_, _domain=domain_, offset=offset,
                      count='1')).json()
    try:
        if posts['response']['items'][0]['is_pinned'] == 1:
            return requests.get(get_post_link(_id=owner_, _domain=domain_, offset='1', count='1')).json()
    except KeyError:
        return posts
    except IndexError:
        print("Group haven't posts yet")


def get_post_text(owner_id_, domain_):
    first_post_ = get_first_post(owner_=owner_id_, domain_=domain_)
    attachments = first_post_['response']['items'][0]['attachments']
    additional_text = first_post_['response']['items'][0]['text']
    try:
        type_post = attachments[0]['type']
        post = attachments[0][type_post]['description']
        return post + '\n' + additional_text
    except KeyError:
        return additional_text
    except IndexError:
        return additional_text


def get_owner_id(link):
    name = link.replace('https://vk.com/', '', 1)
    return '-' + str(requests.get(
        'https://api.vk.com/method/utils.resolveScreenName?screen_name=' + name + '&access_token=50934c3550934c3550934c354550e8167b5509350934c353283b43e2d4451cd19e0fafb&v=5.131').json()[
                         'response']['object_id'])


# print(get_first_post(owner_id='-38029', domain='https://vk.com/synergyuniversity')['response']['items'][0]['id'])


def write_ids_file(now_domain, orig_file, new_id):
    if orig_file.find(now_domain + ' = ') != -1:  # если есть домен и id, то вывести id
        post_ids = orig_file.split('  ')
        for z in range(len(post_ids)):
            if post_ids[z].find(now_domain + ' = ') != -1:
                return post_ids[z].replace(now_domain + ' = ', '', 1)
    else:  # если нет домена, то записать домен
        f1 = open('postIdis.txt', 'r', encoding="utf-8").read()
        with open('postIdis.txt', 'w') as ff:
            ff.write(f1 + str(now_domain) + ' = ' + str(new_id) + '  ')
        return 1


def write_new_id(link, num):
    f1 = open('postIdis.txt', 'r', encoding="utf-8").read()
    split = f1.split('  ')
    for j in range(len(split)):
        if split[j].find(link) != -1:
            f1 = f1.replace(split[j] + '  ', link + ' = ' + str(num) + '  ', 1)
    with open('postIdis.txt', 'w') as ff:
        ff.write(f1)


def post_id_check():
    ids_text = open('postIdis.txt', 'r', encoding="utf-8").read()
    ids = ids_text.split('  ')
    groups = open('groups.txt', 'r', encoding="utf-8").read()
    for i in range(len(ids)):
        if groups.find(re.sub(r' = \d+', '', ids[i])) == -1:
            with open('postIdis.txt', 'w') as ff:
                ff.write(ids_text.replace(ids[i] + '  ', '', 1))


def main():
    while True:
        post_id_check()
        time.sleep(1)
        f = open('postIdis.txt', 'r', encoding="utf-8").read()
        domains = open('groups.txt', 'r', encoding="utf-8").read().split(' ')
        for x in range(len(domains)):
            domain = domains[x]
            owner_id = get_owner_id(domain)
            time.sleep(1)
            first_post = get_first_post(owner_=owner_id, domain_=domain)
            post_text = get_post_text(owner_id_=owner_id, domain_=domain)
            current_id = first_post['response']['items'][0]['id']
            post_id = write_ids_file(domain, f, current_id)
            if int(post_id) != int(current_id) or post_id == 1:
                write_new_id(domain, current_id)
                file = open('keywords.txt', 'r', encoding="utf-8").read().lower()
                keywords = file.split(' ')
                keywords_mention = 0
                for i in range(len(keywords)):
                    if post_text.lower().find(keywords[i]) != -1:
                        keywords_mention += 1
                if keywords_mention >= len(keywords):
                    mass_message(keyword=keywords[0], group_link=domain, group_id=owner_id, post_id=current_id)
            time.sleep(2)
        # print(get_post_text(owner_id='-38029', domain='https://vk.com/synergyuniversity'))
        time.sleep(2)


th1 = Thread(target=bot_main).start()
th2 = Thread(target=main).start()
