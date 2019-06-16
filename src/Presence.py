'''
Created on 31.05.2019

@author: Christian Kuster
'''

from slacker import Slacker

from flask import Flask, request, make_response

import json, os

from apscheduler.schedulers.background import BackgroundScheduler

# Flask web server for incoming traffic from Slack
app = Flask(__name__)

slack = Slacker(os.environ['app-token'])

# Get users list
response = slack.users.list()
users = response.body['members']

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
    slack.chat.post_message(channel = '@kuster', as_user = True, text = 'Pick an item from the dropdown list', blocks = '[     {    "type": "section",    "text": {    "type": "mrkdwn",    "text": "Pick an item from the dropdown list"    },    "accessory": {    "type": "static_select",    "placeholder": {    "type": "plain_text",    "text": "Select an item",    "emoji": true    },    "options": [    {    "text": {    "type": "plain_text",    "text": "Choice 1",    "emoji": true    },    "value": "value-0"    },    {    "text": {    "type": "plain_text",    "text": "Choice 2",    "emoji": true    },    "value": "value-1"    },    {    "text": {    "type": "plain_text",    "text": "Choice 3",    "emoji": true    },    "value": "value-2"    }    ]    }     } ]')

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=ask, trigger='cron', second='0')
    scheduler.start()
    app.run(debug=True, use_reloader=False, host='0.0.0.0')