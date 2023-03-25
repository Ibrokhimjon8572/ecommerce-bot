import logging
import json
import telebot
from telebot import types

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .control import Control

BOT_TOKEN = getattr(settings, "BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# Create your views here.

@csrf_exempt
def set_webhook(request: HttpRequest):
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
        logging.info(update)
        bot.process_new_updates([update])
        return HttpResponse(status=200)

@bot.message_handler(commands=['start'])
def handle_start(msg: types.Message):
    Control().handle_start(msg)