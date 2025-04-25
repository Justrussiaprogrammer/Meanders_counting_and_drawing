import BotTG.functions_private as func_private
import Meanders.functions_meanders as functions
import texts

import sqlite3
import telebot
from telebot import types
import yaml


f = open("config.yaml", "r")
conf = yaml.safe_load(f)
f.close()
bot = telebot.TeleBot(conf["token"])


@bot.message_handler(commands=['admin'])
def my_admin(message):
    write_text(message.chat.id, lines.reboot_text)


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
        write_text(message.chat.id, lines.help_text_admin)
    else:
        write_text(message.chat.id, lines.help_text)


@bot.message_handler(commands=['get_game'])
def my_get_game(message):
    fd_for_out = open("../game.zip", "rb")
    bot.send_document(message.chat.id, fd_for_out)
    fd_for_out.close()


@bot.message_handler(commands=['reboot'])
def my_reboot(message):
    func_private.__reboot(message.chat.id)
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

    if message.chat.id == conf["owner"]:
        write_text(message.chat.id, lines.start_text_admin)
    elif message.chat.id in conf["admins"]:
        write_text(message.chat.id, lines.start_text_admin)
    else:
        write_text(message.chat.id, lines.start_text)


    func_private.__reboot(message.chat.id)


def write_text(name_id, string, user=True):
    fd = open("log.txt", 'a')
    if user:
        fd.write(f"name_id: {name_id}; answer: {string}\n")
        bot.send_message(name_id, string, reply_markup=types.ReplyKeyboardRemove())
    else:
        fd.write(f"name_id: {name_id}; request: {string}\n")
    fd.close()


@bot.message_handler(content_types=['text'])
def error_manager(message):
    global conf

    write_text(message.chat.id, message.text, user=False)
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
                flag = functions.Meanders(len(ints)).is_meander(ints)
                if flag:
                    write_text(message.chat.id, lines.meander_positive_text)
                else:
                    write_text(message.chat.id, lines.meander_negative_text)

                cursor.execute('UPDATE Users SET action = ? WHERE user_id = ?', (0, message.chat.id))
                connection.commit()
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
