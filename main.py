import hashlib
from datetime import date
import cryptocode
import os
import shutil
from operator import itemgetter


# добавляем нового пользователя
def new_user():
    """Создает нового пользователя и записывает данные в файл с пользователями"""
    new_login = input('\n Введите имя пользователя: ')
    if validation_user(new_login):
        new_password = input('\n Введите пароль: ')
        hash_password = hashlib.sha256(new_password.encode()).hexdigest()
        with open('users.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{new_login} {hash_password}\n')
    else:
        print('\n Такой пользователь существует!')


# создаем список из списков с именами полльзователей и хэшей паролей
def users_to_list():
    """Читает файл c пользователями. Создает словарь с позьзователями и хешами паролей."""
    with open(f'users.txt', 'r', encoding='UTF-8') as file:
        text = file.read().split('\n')
    dict_all = {}
    for i in text:
        if len(i) > 0:
            list_user = i.split(' ')
            dict_user = {list_user[0]: list_user[1]}
            dict_all.update(dict_user)
    return dict_all


# проверяем имя пользователя на оригинальность
def validation_user(user: str):
    """Проверяет имя пользователя на оригинальность"""
    if users_to_list().get(user):
        return False
    return user


# получить хэш пароля выбранного пользователя
def take_hash(user: str):
    """Возвращает хеш выбранного пользователя"""
    return users_to_list().get(user)


# авторизация пользователя
def authorization():
    """Заправшивает логин и пороль, сверяет и возвращает True/False"""
    user = input('\n Введите логин: ')
    if not validation_user(user) and user == 'admin':
        password = input('\n Введите пароль: ')
        if take_hash(user) == hashlib.sha256(password.encode()).hexdigest():
            return 'admin'
        else:
            print('\n Неверный пароль!')
    elif not validation_user(user):
        password = input('\n Введите пароль: ')
        if take_hash(user) == hashlib.sha256(password.encode()).hexdigest():
            return 'user'
        else:
            print('\n Неверный пароль')
    else:
        print('\n Неверное имя пользователя')
    return False


# создание заметки
def create_notes():
    """Создает заметку, шифрует и помещает ее в файл с заметками"""
    title = encode_notes(input('\n Введите название заметки: '))
    text = encode_notes(input('\n Введите текст заметки: '))
    data = encode_notes(str(date.today()))
    if len(title) > 75 and len(text) > 75:
        with open('notes.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{data} {title} {text}\n')
        print('\n Заметка добавлена')
    else:
        print('\n\n Заметка не может быть пустой!')


# шифратор и дешифратор заметок
def encode_notes(text: str):
    """Кодирует текст по ключу"""
    return cryptocode.encrypt(text, "code")


def decoded_notes(text: str):
    """Декодирует текст по ключу"""
    return cryptocode.decrypt(text, "code")


# показать заметки
def show_notes():
    """Расшифровывает текст с заметками и выводит список со списками заметок"""
    with open('notes.txt', 'r', encoding='UTF-8') as file:
        text = file.read()
    all_notes = []
    notes = text.split('\n')
    for note in notes:
        if len(note) > 0:
            note = note.split()
            list_nodes = [decoded_notes(note[0]), decoded_notes(note[1]), decoded_notes(note[2])]
            all_notes.append(list_nodes)
    return all_notes


# список пользователей
def show_list_users():
    """Возвращает список пользователей"""
    print('\n')
    for v, i in enumerate(users_to_list(), 1):
        print(' ', v, i)


# очистка консоли и вывод названия программы
def clear_console():
    """Очищает консоль и выводин название программы"""
    os.system('cls')
    print('{{:-^{}}}'.format(shutil.get_terminal_size().columns).format('SECRET_NOTES'))


# главное меню
def main_menu():
    """Отображает главное меню программы"""
    while True:
        clear_console()
        user = authorization()
        if user == 'admin':
            admin_menu()
        elif user == 'user':
            users_menu()
        else:
            print('\n Нажмите <Enter> для продолжения. ')
            input()


# режим администратора
def admin_mode():
    """Очищает консоль и выводит на экран строки SECRET_NOTES и режим администратора"""
    os.system('cls')
    print('{{:-^{}}}'.format(shutil.get_terminal_size().columns).format('SECRET_NOTES'))
    print('{{:*^{}}}'.format(shutil.get_terminal_size().columns).format(' режим администратора '))


# меню для админа
def admin_menu():
    """Отображает меню для admin"""
    admin_mode()
    while True:
        admin_mode()
        print(
            ' \n Главное меню\n\n 1. Просмотреть заметки\n 2. Добавить заметку\n '
            '3. Сменить пользователя\n 4. Добавить нового пользователя\n 5. Показать пользователей')
        select_menu_item = input('\n\n Выбирете пункт меню: ')
        if select_menu_item == '1':
            admin_mode()
            print('\n Заметки\n')
            for i in show_notes():
                print(i)
            while True:
                print('\n\n 1. Отсортировать по дате\n 2. Отсортировать по названию\n 3. Найти по названию\n '
                      '4. Выйти в главное меню\n')
                select_menu_notes_item = input('\n\n Выбирете пункт меню: ')
                if select_menu_notes_item == '1':
                    admin_mode()
                    print('\n Заметки (сортировка по дате)\n')
                    for j in sort_title_notes(0):
                        print(j)
                elif select_menu_notes_item == '2':
                    admin_mode()
                    print('\n Заметки (сортировка по названию)\n')
                    for k in sort_title_notes(1):
                        print(k)
                elif select_menu_notes_item == '3':
                    admin_mode()
                    print('\n Поиск заметок\n')
                    search_notes()
                    print('\n Нажмите <Enter> для продолжения.')
                    input()
                    break
                elif select_menu_notes_item == '4':
                    break
                else:
                    print('\n\n Ошибка выбора. Нажмите <Enter> для продолжения.')
                    input()
        elif select_menu_item == '2':
            admin_mode()
            print('\n Новая заметка')
            create_notes()
            print('\n\n Нажмите <Enter> для выхода в меню.')
            input()
        elif select_menu_item == '3':
            break
        elif select_menu_item == '4':
            admin_mode()
            print('\n Новый пользователь')
            new_user()
            print('\n\n Пользователь добавлен. Нажмите <Enter> для продолжения.')
            input()
        elif select_menu_item == '5':
            admin_mode()
            print('\n Список пользователей')
            show_list_users()
            print('\n\n Нажмите <Enter> для продолжения.')
            input()
        else:
            print('\n\n Ошибка выбора. Нажмите <Enter> для продолжения.')
            input()


# меню для авторизованных пользователей
def users_menu():
    """Отображает меню для авторизованных пользователей"""
    clear_console()
    while True:
        clear_console()
        print('\n Главное меню\n\n 1. Просмотреть заметки\n 2. Добавить заметку\n 3. Сменить пользователя')
        select_menu_item = input('\n\n Выбирете пункт меню: ')
        if select_menu_item == '1':
            clear_console()
            print('\n Заметки\n')
            for i in show_notes():
                print(i)
            while True:
                print('\n\n 1. Отсортировать по дате\n 2. Отсортировать по названию\n 3. Найти по названию\n '
                      '4. Выйти в главное меню\n')
                select_menu_notes_item = input('\n\n Выбирете пункт меню: ')
                if select_menu_notes_item == '1':
                    clear_console()
                    print('\n Заметки (сортировка по дате)\n')
                    for j in sort_title_notes(0):
                        print(j)
                elif select_menu_notes_item == '2':
                    clear_console()
                    print('\n Заметки (сортировка по названию)\n')
                    for k in sort_title_notes(1):
                        print(k)
                elif select_menu_notes_item == '3':
                    clear_console()
                    print('\n Поиск заметок\n')
                    search_notes()
                    print('\n\n Нажмите <Enter> для продолжения.')
                    input()
                    break
                elif select_menu_notes_item == '4':
                    break
                else:
                    print('\n\n Ошибка выбора. Нажмите <Enter> для продолжения.')
                    input()
        elif select_menu_item == '2':
            clear_console()
            print('\n Новая заметка')
            create_notes()
            print('\n\n Нажмите <Enter> для выхода в меню.')
            input()
        elif select_menu_item == '3':
            break
        else:
            print('\n\n Ошибка выбора. Нажмите <Enter> для продолжения.')
            input()


# сортировка заметок по названию (index == 1) и дате (index == 0)
def sort_title_notes(index: int):
    """В зависимости от выбранного параметра сортирует заметки по дате либо по названию"""
    lst = show_notes()
    lst.sort(key=itemgetter(index))
    return lst


# поиск заметок по названию
def search_notes():
    """Выводит искомую заметку или возвращает False"""
    title_notes = input('\n Введите название заметки: ')
    list_notes = show_notes()
    for i in range(len(list_notes)):
        if list_notes[i][1].count(title_notes):
            print('\n Заметка найдена\n')
            print(list_notes[i])
            break
    else:
        print('\n Заметка не найдена\n')


if __name__ == '__main__':
    main_menu()


