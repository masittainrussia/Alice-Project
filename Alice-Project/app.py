from flask import Flask, request
import json
from bs4 import BeautifulSoup
import requests
import Levenshtein as lv
from data import db_session
from data.models import Item, Place

app = Flask(__name__)
users_sesison = {}
users_things = {}


@app.route('/post', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    text = request.json['request']['original_utterance']
    text = text.lower()
    user_id = request.json['session']['user_id']

    if text == 'ничего':
        response['response']['text'] = "Надеюсь вы больше не будете терять свои вещи. Досвидания!"
        response['response']['end_session'] = True
        del users_sesison[user_id]
        return json.dumps(response)

    if user_id not in users_sesison:
        response['response']['text'] = "Привет, это Алиса! Что у тебя потерялось?"
        users_sesison[user_id] = 'start'
    else:
        if not found(text):
            if users_sesison[user_id] == "start":
                item_id = get_id(text)
                print(item_id)

                if item_id:
                    session = db_session.create_session()
                    thing = session.query(Item).filter(Item.id == item_id).first()
                    places = [i.place for i in thing.places]
                    response['response']['text'] = places[0]
                    users_sesison[user_id] = places[1:]
                    users_things[user_id] = thing.item
                else:
                    link = "https://market.yandex.ru/search?text=" + text
                    response['response']['text'] = \
                        "Ой, я не знаю где это может быть. Стоит спросить у мамы, она точно знает! Ну или на крайний случай посмотри тут: " + link + '\n' + "Что еще у тебя потерялось?"
                    users_sesison[user_id] = 'start'
            else:
                if str(type(users_sesison[user_id])) == "<class 'list'>":
                    if len(users_sesison[user_id]) > 0:
                        things = users_sesison[user_id]
                        users_sesison[user_id] = things[1:]
                        response['response']['text'] = things[0]
                    else:
                        link = "https://market.yandex.ru/search?text=" + users_things[user_id]
                        response['response']['text'] = "Стоит спросить у мамы, она точно знает! Ну или на крайний случай посмотри тут:" + link + '\n' + "Что еще у тебя потерялось?"
                        users_sesison[user_id] = 'start'
                else:
                    if users_sesison[user_id]:
                        pass
        else:
            response['response']['text'] = "Что еще у тебя потерялось?"
            users_sesison[user_id] = 'start'

    return json.dumps(response)



def get_synonym(word):
    link = "https://synonymonline.ru/" + word[0].upper() + "/" + word.lower()
    page_response = requests.get(link)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    res = page_content.find_all(class_="col-sm-4 col-xs-6")
    synonyms = [str(line)[36:-12] for line in res]
    return synonyms


def get_id(word):
    synonims = get_synonym(word)
    synonims.append(word)
    result = [0, 0] # расстояние Левенштейна и id
    session = db_session.create_session()
    for s in synonims:
        result = session.query(Item).filter(Item.item == s).first()
        if result:
            return result.id
    return ''


def found(word):
    may_be = ['нашел', 'нашлось', 'ура']
    max_dist = 0
    for m in may_be:
        if lv.ratio(word, m) > max_dist:
            max_dist = lv.ratio(word, m)
    print(max_dist)
    if max_dist >= 0.55:
        return True
    return False


def main():
    db_session.global_init("base.sqlite")
    app.run()


if __name__ == '__main__':
    main()