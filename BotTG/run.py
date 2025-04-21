import json
import functions
import sqlite3
import telebot
from telebot import types
import texts
import yaml


f = open("config.yaml", "r")
conf = yaml.safe_load(f)
f.close()
bot = telebot.TeleBot(conf["token"])


if __name__ == '__run__':
    f = open('config.yaml', 'r')
    conf = yaml.safe_load(f)
    f.close()

    lines = texts.Texts()
    data, local_data, error_text, name_digit, digit_name, errors_list = functions.__reboot()

    bot.polling(none_stop=True)
