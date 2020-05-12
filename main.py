from flask import Flask
from flask import request
import json

from . import db_session

app = Flask(__name__)
db_session.global_init("db/blogs.sqlite")

@app.route('/post', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    return json.dumps(response)


def handle_dialog(res, req):
    if req['request']['original_utterance']:
        item = morph.parse(req['request']['original_utterance'])[0]
        pad, number, gend = item.tag.case, item.tag.number, item.tag.gender
        lost_word = (morph.parse('потерять')[0]).inflect({'VERB', pad, gend, number})
        res['response']['text'] = f'У тебя {lost_word} {item.word}?'
    else:
        res['response']['text'] = "Привет, это Алиса! Что у тебя потерялось?"


if __name__ == '__main__':
    app.run()