'''
Created on 31.05.2019

@author: Christian Kuster
'''

from slacker import Slacker#, Bots

from flask import Flask, request, make_response

import json, os, datetime#, locale

from apscheduler.schedulers.background import BackgroundScheduler

# Flask web server for incoming traffic from Slack
app = Flask(__name__)

slack = Slacker(os.environ['app-token'])

places = ["Köln", "Münster", "Remote"]

# retrieve users
users = []
for member in filter(lambda x: x['id'] != 'USLACKBOT' and not x['is_bot'] and not x['deleted'], slack.users.list().body['members']):
    users.append(member['name'])

#slack.dialog.open('[     {    "type": "section",    "text": {    "type": "mrkdwn",    "text": "Pick an item from the dropdown list"    },    "accessory": {    "type": "static_select",    "placeholder": {    "type": "plain_text",    "text": "Select an item",    "emoji": true    },    "options": [    {    "text": {    "type": "plain_text",    "text": "Choice 1",    "emoji": true    },    "value": "value-0"    },    {    "text": {    "type": "plain_text",    "text": "Choice 2",    "emoji": true    },    "value": "value-1"    },    {    "text": {    "type": "plain_text",    "text": "Choice 3",    "emoji": true    },    "value": "value-2"    }    ]    }     } ]', 39393)

@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    # Parse the request payload
    message_action = json.loads(request.form["payload"])
    print(message_action)
    actions = message_action['actions']
    for action in actions:
        action_type = action['type']
        if action_type == 'static_select':
            print(action["selected_option"]["text"]["text"])
    return make_response("", 200)

def ask():
    """Send users question"""
    
    d = datetime.date.today()
    dow = []
    for x in range(3, 8):
        dow.append((d + datetime.timedelta(days=x)).strftime("%A - %x"))
    
    blocks_object = [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Hi!\nWhere will you be working next week?",
                "emoji": True
            }
        }]
    
    place_options = []
    for place in places:
        place_options.append({
                "text": {
                    "type": "plain_text",
                    "text": place,
                    "emoji": True
                },
                "value": place
            })
    
    for day in dow:
        blocks_object.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*" + day + "*"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True
                    },
                    "options": place_options
                }
            })
    
    slack.chat.post_message(channel = '@kuster', as_user = True, text = 'Where will you be working next week?', blocks = json.dumps(blocks_object))

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
#     scheduler.add_job(func=ask, trigger='cron', day_of_week='fri', hour='9', minute='30')
    scheduler.add_job(func=ask, trigger='cron', minute='*/2')
    scheduler.start()
    app.run(debug=True, use_reloader=False, host='0.0.0.0')