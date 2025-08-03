import os


def write_list_of_items_in_file(list_of_names, path):
    check_path('data')
    with open(path, 'w', encoding='utf-8') as f:
        for item in list_of_names:
            f.write(str(item) + '\n')


def read_list_of_items_in_file(path):
    check_path('data')
    with open(path, mode='r', encoding='utf-8') as f:
        list_items = []
        for line in f:
            list_items.append(line.replace('\n', ''))
    return list_items


def get_list_items_in_file(path):
    try:
        list_items = read_list_of_items_in_file(path)
    except FileNotFoundError:
        list_items = []
        write_list_of_items_in_file(list_items, path)
    return list_items


def check_path(path):
    current_path = os.getcwd()
    path = os.path.join(current_path, path)
    if not os.path.exists(path):
        os.makedirs(path)
