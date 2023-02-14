import os
import json
import requests

LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_REPLY_ENDPOINT = os.getenv('LINE_REPLY_ENDPOINT')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_COMPLETIONS_ENDPOINT = os.getenv('OPENAI_COMPLETIONS_ENDPOINT')

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

def openai_completions(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(OPENAI_API_KEY)
    }
    data = {
        "model": "text-davinci-003",
        "prompt": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\n"
        + "Human: Hello, who are you?\n"
        + "AI: I am an AI created by OpenAI. How can I help you today?\n"
        + "Human: " + prompt
        + "\nAI:",
        "temperature": 0.9,
        "max_tokens": 100,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0.6,
    }
    try:
        print('OpenAI request: {}'.format(prompt))
        openai_response = requests.post(OPENAI_COMPLETIONS_ENDPOINT, headers=headers, data=json.dumps(data))
        print('OpenAI response: {}'.format(openai_response.json()))
        return openai_response.json()['choices'][0]['text']
    except:
        return 'OpenAIが壊れてました😢'

def lambda_handler(event, context):
    
    message = json.loads(event['body'])['events'][0]['message']['text']
    reply_token = json.loads(event['body'])['events'][0]['replyToken']

    openai_response = openai_completions(message)
    
    line_reply(reply_token, openai_response)
    return {
        'statusCode': 200
    }
