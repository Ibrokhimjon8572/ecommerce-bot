import json
import telebot

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .handlers import bot
import os
import logging

# Create your views here.


@csrf_exempt
def set_webhook(request: HttpRequest):
    if os.getenv("ENVIRONMENT") != "dev":
        return JsonResponse(status=400, data={
            'status': False,
            'message': 'Allowed only in development',
        })
    bot.remove_webhook()
    if request.method != "POST":
        return JsonResponse(status=400, data={
            'status': False,
            'message': 'Only post method is allowed',
        })

    body = json.loads(request.body)
    return JsonResponse(status=200, data={
        'status': bot.set_webhook(f"https://{body['url']}/bot/"),
    })


@csrf_exempt
def index(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponse("Telegram Bot")
    if request.method == 'POST':
        update = telebot.types.Update.de_json(
            request.body.decode("utf-8"))
        try:
            bot.process_new_updates([update])
        except Exception as e:
            logging.error(e)
        return HttpResponse(status=200)
