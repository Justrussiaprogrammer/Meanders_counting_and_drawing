import yaml
import sqlite3

def __reboot(id):
    # fd = open('info.json')
    # data = json.load(fd)
    # fd.close()
    # fd = open('config.yaml', 'r')
    # conf = yaml.safe_load(fd)
    # fd.close()

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET level = ? WHERE user_id = ?', (0, id))
    cursor.execute('UPDATE Users SET search_error = ? WHERE user_id = ?', (0, id))
    cursor.execute('UPDATE Users SET action = ? WHERE user_id = ?', (0, id))
    connection.commit()
    connection.close()
