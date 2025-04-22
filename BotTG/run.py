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

@bot.message_handler(commands=['start'])
def my_start(message):
    write_text(message.chat.id, lines.start_text)


@bot.message_handler(commands=['help'])
def my_help(message):
    if message.chat.id in conf["admins"]:
        write_text(message.chat.id, lines.help_admin_text)
    else:
        write_text(message.chat.id, lines.help_text)


@bot.message_handler(commands=['check'])
def my_check(message):
    all_meanders = functions.Meanders(10).get_all_meanders()

    write_text(message.chat.id, lines.check_text)


def write_text(name_id, string):
    # fd = open("log.txt", 'a')
    # fd.write(string + '\n')
    # fd.close()
    bot.send_message(name_id, string, reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    lines = texts.Texts()
    # data, local_data, error_text, name_digit, digit_name, errors_list = functions.__reboot()

    bot.polling(none_stop=True)
