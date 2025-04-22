import yaml

def __reboot():
    # fd = open('info.json')
    # data = json.load(fd)
    # fd.close()
    # fd = open('config.yaml', 'r')
    # conf = yaml.safe_load(fd)
    # fd.close()

    local_data = dict()
    error_text = dict()
    name_digit = dict()
    name_digit["0"] = 0
    name_digit["Добавить ошибку"] = -2
    name_digit["Обновить описание"] = -1
    digit_name = dict()
    digit_name[0] = 0
    digit_name[-2] = "Добавить ошибку"
    digit_name[-1] = "Обновить описание"
    errors_list = dict()

    return local_data, error_text, name_digit, digit_name, errors_list
