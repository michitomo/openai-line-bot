import os
import json
import requests

LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_REPLY_ENDPOINT = os.getenv('LINE_REPLY_ENDPOINT')

def line_reply(reply_token, response):
    Authorization = 'Bearer {}'.format(LINE_CHANNEL_ACCESS_TOKEN)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    data = {
        "replyToken": reply_token,
        "messages": [{
                        "type":"text",
                        "text":response
                    }]
        }
    r = requests.post(LINE_REPLY_ENDPOINT, headers=headers, data=json.dumps(data))
    print('LINE response: {}'.format(r.json()))

def lambda_handler(event, context):
    
    message = json.loads(event['body'])['events'][0]['message']['text']
    reply_token = json.loads(event['body'])['events'][0]['replyToken']
    
    line_reply(reply_token, message)
    return {
        'statusCode': 200
    }
