import json
import functions
import BotTG.bot_functions as bot_func
import sqlite3
import telebot
from telebot import types
import texts
import yaml

from functions import Meanders

f = open("config.yaml", "r")
conf = yaml.safe_load(f)
f.close()
bot = telebot.TeleBot(conf["token"])

@bot.message_handler(commands=['check'])
def my_check(message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET action = ? WHERE user_id = ?', (1, message.chat.id))
    connection.commit()
    write_text(message.chat.id, lines.check_text)

@bot.message_handler(commands=['help'])
def my_help(message):
    if message.chat.id in conf["admins"]:
        write_text(message.chat.id, lines.help_admin_text)
    else:
        write_text(message.chat.id, lines.help_text)

@bot.message_handler(commands=['reboot'])
def my_reboot(message):
    bot_func.__reboot(message.chat.id)
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

    bot_func.__reboot(message.chat.id)


def write_text(name_id, string):
    fd = open("log.txt", 'a')
    fd.write("name_id:" + str(name_id) + "; message: " + string + '\n')
    fd.close()
    bot.send_message(name_id, string, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def error_manager(message):
    global conf

    connection = sqlite3.connect('database.db')
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT level, search_error, action FROM Users WHERE user_id = ?', (message.chat.id,))
        results = cursor.fetchall()[0]
        rank = results[0]
        search_error = int(results[1])
        action = results[2]
        match action:
            case 0:
                write_text(message.chat.id, lines.no_action_text)
            case 1:
                ints = [int(x) for x in message.text.split()]
                meanders = Meanders(len(ints)).get_all_meanders()
                cursor.execute('UPDATE Users SET action = ? WHERE user_id = ?', (0, message.chat.id))
                connection.commit()
                if ints in meanders:
                    write_text(message.chat.id, lines.meander_positive_text)
                else:
                    write_text(message.chat.id, lines.meander_negative_text)
    except IndexError:
        write_text(message.chat.id, lines.index_error_text)
    except ValueError:
        write_text(message.chat.id, lines.value_error_text)
    except Exception:
        write_text(message.chat.id, lines.fatal_text)
    finally:
        connection.close()


if __name__ == '__main__':
    lines = texts.Texts()

    bot.polling(none_stop=True)
