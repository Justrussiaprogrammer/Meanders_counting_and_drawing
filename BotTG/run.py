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


def build_keyboard(message, this_dict, string):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for key in this_dict:
        new_btn = types.KeyboardButton(digit_name[key])
        markup.add(new_btn)

    bot.send_message(message.chat.id, string, reply_markup=markup)


@bot.message_handler(commands=['answer'])
def my_answer(message):
    fd = open('offers.json')
    data = json.load(fd)
    fd.close()
    write_text(message.chat.id, str(data))


@bot.message_handler(commands=['file'])
def my_file(message):
    global data

    fd = open('result.txt', 'w')
    fd.close()
    functions.write_to_file('result.txt', data, 0)

    fd_for_out = open("./result.txt", "rb")
    bot.send_document(message.chat.id, fd_for_out)
    fd_for_out.close()


@bot.message_handler(commands=['fix'])
def my_fix(message):
    global local_data

    if message.chat.id in conf["admins"]:
        local_data = data

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE Users SET action = ? WHERE user_id = ?', (1, message.chat.id))
        connection.commit()
        connection.close()

        build_keyboard(message, [-2] + errors_list[0], lines.add_text)
    else:
        write_text(message.chat.id, lines.no_admin_text)


@bot.message_handler(commands=['get'])
def my_get(message):
    build_keyboard(message, errors_list[0], lines.keyboard_text)


@bot.message_handler(commands=['help'])
def my_help(message):
    if message.chat.id in conf["admins"]:
        write_text(message.chat.id, lines.help_admin_text)
    else:
        write_text(message.chat.id, lines.help_text)


@bot.message_handler(commands=['offer'])
def my_offer(message):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET action = ? WHERE user_id = ?', (4, message.chat.id))
    connection.commit()
    connection.close()
    write_text(message.chat.id, lines.offer_text)


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

    data, local_data, error_text, name_digit, digit_name, errors_list = functions.__reboot()
    write_text(message.chat.id, lines.reboot_text)


def write_text(name_id, string):
    fd = open("log.txt", 'a')
    fd.write(string + '\n')
    fd.close()
    bot.send_message(name_id, string, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def error_manager(message):
    global conf, local_data

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
                word = name_digit[message.text]
                if word in errors_list[search_error]:
                    write_text(message.chat.id, error_text[word])
                    if word in errors_list:
                        rank += 1
                        build_keyboard(message, errors_list[word], lines.keyboard_text)

                        cursor.execute('UPDATE Users SET search_error = ? WHERE user_id = ?', (word, message.chat.id))
                        connection.commit()
                    else:
                        cursor.execute('UPDATE Users SET search_error = ? WHERE user_id = ?', (0, message.chat.id))
                        connection.commit()
                        rank = 0
                        my_get(message)
                    cursor.execute('UPDATE Users SET level = ? WHERE user_id = ?', (int(rank), message.chat.id))
                    connection.commit()
                else:
                    write_text(message.chat.id, lines.hack_text)
            case 1:
                word = name_digit[message.text]
                if word < 0:
                    cursor.execute('UPDATE Users SET search_error = ? WHERE user_id = ?', (word, message.chat.id))
                    cursor.execute('UPDATE Users SET action = ? WHERE user_id = ?', (2, message.chat.id))
                    connection.commit()
                    if word == -2:
                        write_text(message.chat.id, lines.name_text)
                    else:
                        write_text(message.chat.id, functions.get_error_text(local_data["text"]))
                        write_text(message.chat.id, lines.info_text)
                elif word in errors_list[search_error]:
                    if rank == 0:
                        local_data = local_data[message.text]
                    else:
                        local_data = local_data["next"][message.text]
                    rank += 1
                    cursor.execute('UPDATE Users SET level = ? WHERE user_id = ?', (int(rank), message.chat.id))
                    cursor.execute('UPDATE Users SET search_error = ? WHERE user_id = ?', (word, message.chat.id))
                    connection.commit()
                    if word in errors_list:
                        build_keyboard(message, [-2, -1] + errors_list[word], lines.keyboard_text)
                    else:
                        build_keyboard(message, [-2, -1], lines.keyboard_text)
                else:
                    write_text(message.chat.id, lines.hack_text)
            case 2:
                if search_error == -2:
                    if rank == 0:
                        local_data[message.text] = {"text": "", "status": 1, "next": {}}
                        if len(local_data) >= conf["base"]:
                            conf["base"] *= 2
                        local_data = local_data[message.text]
                    else:
                        local_data["next"][message.text] = {"text": "", "status": 1, "next": {}}
                        if len(local_data["next"]) >= conf["base"]:
                            conf["base"] *= 2
                        local_data = local_data["next"][message.text]
                    write_text(message.chat.id, lines.instruction_text)
                    fd = open('test.yaml', 'w')
                    yaml.dump(conf, fd)
                    fd.close()
                    cursor.execute('UPDATE Users SET action = ? WHERE user_id = ?', (3, message.chat.id))
                    connection.commit()
                else:
                    local_data["text"] = message.text
                    write_text(message.chat.id, lines.name_end_text)
                    fd = open('info.json', 'w')
                    json.dump(data, fd, ensure_ascii=False, indent=2)
                    fd.close()
                    my_reboot(message)
            case 3:
                local_data["text"] = message.text
                write_text(message.chat.id, lines.name_end_text)
                fd = open('info.json', 'w')
                json.dump(data, fd, ensure_ascii=False, indent=2)
                fd.close()
                my_reboot(message)
            case 4:
                for name_id in conf["admins"]:
                    write_text(name_id, functions.do_offer_text(message))
                cursor.execute('UPDATE Users SET action = ? WHERE user_id = ?', (0, message.chat.id))
                connection.commit()
                write_text(message.chat.id, "Ваше сообщение было доставлено\n")
    except IndexError:
        write_text(message.chat.id, lines.index_error_text)
    except Exception:
        write_text(message.chat.id, lines.fatal_text)
    finally:
        connection.close()


if __name__ == '__run__':
    f = open('config.yaml', 'r')
    conf = yaml.safe_load(f)
    f.close()

    lines = texts.Texts()
    data, local_data, error_text, name_digit, digit_name, errors_list = functions.__reboot()

    bot.polling(none_stop=True)
