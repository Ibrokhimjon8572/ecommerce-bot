import requests
import json
import telebot

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .control import bot

BOT_TOKEN = getattr(settings, "BOT_TOKEN")

# Create your views here.

@csrf_exempt
def set_webhook(request: HttpRequest):
    global ok
    if request.method != "POST":
        return JsonResponse(status=400, data={
            'status': False,
            'message': 'Only post method is allowed',
        })

    body = json.loads(request.body)
    r = requests.get('https://api.telegram.org/bot' + BOT_TOKEN +
            '/setwebhook?url=https://' + body['url'] + '/bot/')
    res = r.json()
    return JsonResponse(status=200, data={
        'status': True,
        'message': res
    })


@csrf_exempt
def index(request: HttpRequest):
    print(request, request.body, request.headers)
    if request.method == 'GET':
        return HttpResponse("Telegram Bot")
    if request.method == 'POST':
        update = telebot.types.Update.de_json(
                request.body.decode("utf-8"))
        print(update)
        bot.process_new_updates([update])
        return HttpResponse(status=200)