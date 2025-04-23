import json
import functions
import BotTG.bot_functions as bot_func
import sqlite3
import telebot
from telebot import types
import texts
import yaml

f = open("config.yaml", "r")
conf = yaml.safe_load(f)
f.close()
bot = telebot.TeleBot(conf["token"])

@bot.message_handler(commands=['check'])
def my_check(message):
    all_meanders = functions.Meanders(10).get_all_meanders()

    write_text(message.chat.id, lines.check_text)

@bot.message_handler(commands=['help'])
def my_help(message):
    if message.chat.id in conf["admins"]:
        write_text(message.chat.id, lines.help_admin_text)
    else:
        write_text(message.chat.id, lines.help_text)

@bot.message_handler(commands=['reboot'])
def my_reboot(message):
    global data, local_data, error_text, name_digit, digit_name, errors_list

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET level = ? WHERE user_id = ?', (0, message.chat.id))
    cursor.execute('UPDATE Users SET search_error = ? WHERE user_id = ?', (0, message.chat.id))
    cursor.execute('UPDATE Users SET action = ? WHERE user_id = ?', (0, message.chat.id))
    connection.commit()
    connection.close()

    data, local_data, error_text, name_digit, digit_name, errors_list = bot_func.__reboot()
    write_text(message.chat.id, lines.reboot_text)

@bot.message_handler(commands=['start'])
def my_start(message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT level, search_error, action FROM Users WHERE user_id = ?', (message.chat.id,))
    results = cursor.fetchall()

    if not results:
        cursor.execute('INSERT INTO Users (user_id, level, search_error, action) VALUES (?, ?, ?, ?)',
                       (message.chat.id, 0, 0, 0))
        connection.commit()
        print("The end of registration")

    connection.close()
    write_text(message.chat.id, lines.start_text)
    my_reboot(message)


def write_text(name_id, string):
    # fd = open("log.txt", 'a')
    # fd.write(string + '\n')
    # fd.close()
    bot.send_message(name_id, string, reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    lines = texts.Texts()
    data, local_data, error_text, name_digit, digit_name, errors_list = bot_func.__reboot()

    bot.polling(none_stop=True)
