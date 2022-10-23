from functools import wraps

from flask import session, render_template, request, current_app

from sqlprovider import SQLProvider
from db_class import UseDatabase


provider = SQLProvider('sql')
# Создание конфигурационного словаря, для подключения к Базе Данных
config = {'host': 'localhost', 'user': 'root', 'password': '21F2002g', 'database': 'postavki'}


def get_info(sql: str) -> tuple:
    """
    Обращается к базе данных, выполняет переданный SQL запрос и возвращает его результат

    :param sql: SQL запрос, который нужно выполнить
    :type sql: str
    :return:
        Возвращает значения, полученные в результате запроса
    :rtype: tuple
    """
    with UseDatabase(config) as cursor:
        cursor.execute(sql)  # Выполнение SQL запроса
        result = cursor.fetchall()  # Получение результата SQL запроса
    return result


def compare(login: str, password: str) -> str:
    """
    Функция сравнивает полученные логин и пароль со всеми логинами и паролями в БД

    :param login: Логин введенный пользователя
    :type login: str
    :param password: Пароль введенный пользователем
    :type password: str
    :returns:
        :return: Если совпадения найдены,
                 то возваращется роль авторизованного пользователя
        :rtype: str
        :return: Если совпадения не найдены, то возвращается False
        :rtype: bool

    """
    code_pass = password
    code_login = login
    with UseDatabase(config) as cursor:
        if cursor is None:
            raise ValueError('Курсора нет')
        else:
            cursor.execute(provider.get('get.sql'))  # Формирование и выполнение SQL запроса
            result = cursor.fetchall()  # Получение результата SQL запроса
            for x in result:
                if x[1] == code_login and x[2] == code_pass:  # Сравнение полученных логина и пароля
                    role = x[3]  # Получение роли авторизованного сотрудника
                    return role
        return False


# Декоратор
def use_roots(f):
    """
    Декорирует полученную функцию

    :param f: Функция для декорирования
    :return:  Задекорированная функция
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Проверяет права на использование функционала и ограничивает в случае отсутсвия прав
        """
        if "login" not in session:
            return render_template("unlogin.html")  # Если пользователь не авторизован
        if request.endpoint not in current_app.config["ACCESS_CONFIG"][session["role"]]:
            # Если у авторизованного пользователя отсутсвуют права
            # На использование данного функционала
            return render_template("no_roots.html")
        return f(*args, **kwargs)
    return decorated_function


def year_correct(year: str) -> bool:
    """
    Проверка корректного написания года

    :param year: Год, полученный при вводе в форму
    :type year: str
    :returns:
        :return: True, если год введен корректно
        :rtype: bool
        :return: False, если год введен некорректно
        :rtype: bool
    """
    # Количесвто цифр меньше 4, либо присутсвуют другие символы
    if len(year) < 4 or year.isdigit() is False:
        return False
    return True


def month_correct(month: str) -> bool:
    """
    Проверка введенного месяца на корректность

    :param month: Месяц , полученный при вводе в форму
    :type month: str
    :returns:
        :return: True, если месяц введен корректно
        :rtype: bool
        :return: False, если месяц введен некорректно
        :rtype: bool
    """
    # Если присутвуют другие символы,
    # либо число месяца выходит за рамки стандартных
    if month.isdigit() is False or (int(month) < 1 or int(month) > 12):
        return False
    return True


def model(**kwargs) -> list:
    r"""
    Функция, предназначенная для работы с запросами.
    Проверяет введенные на HTML странице аргументы
    И возвращает  результат выбранного запроса

    :param kwargs:

    :keyword arguments:
            * *name* (``str``) --
                Имя SQL файла
            * *month* (``str``) --
                Месяц, введенный в HTML странице
            * *year* (``str``) --
                Год, введенный в HTML странице
            * *days* (``str``) --
                Количество дней, введенное в HTML странице
    :returns:
        :return: [название ошибки, сообщение об ошибке],
                если аргумент введен некорректно
        :rtype: list
        :return: Результат запроса, если в аргуметах запроса
                присутсвует только количество дней, либо
                аргументы отсутсвуют вовсе
        :rtype: tuple
        :return: [результат запроса, название введенного месяца],
                если в аргуметах запроса присутсвуют год и месяц
        :rtype: list
    """
    if 'month' in kwargs and 'year' in kwargs:
        # Массив названий месяцев
        months = ["Январь", "Февраль", "Март",
                  "Апрель", "Май", "Июнь", "Июль", "Август",
                  "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        # Пользователь не ввел месяц
        if not kwargs["month"]:
            return '!'
        # Пользователь ввел месяц некорректно
        elif month_correct(kwargs["month"]) is False:
            return '!'
        # Пользователь не ввел год
        if not kwargs["year"]:
            return "!"
        # Пользователь ввел год некорректно
        elif year_correct(kwargs["year"]) is False:
            return '!'
        else:
            # Формирование выбранного SQL запроса
            sql = provider.get(kwargs["name"]+".sql", month=kwargs["month"], year=kwargs["year"])
            print(sql)
            # Реузльтат SQL запроса
            result = get_info(sql)
            if not result:
                result = 'Not Found'
            return [result, months[int(kwargs["month"])-1]]
    elif 'days' in kwargs:
        # Пользователь не ввел количество дней
        if not kwargs["days"]:
            return '!'
        # Пользователь ввел количество дней некорректно
        elif kwargs["days"].isdigit() is False:
            return '!'
        else:
            # Формирование выбранного SQL запроса
            sql = provider.get(kwargs["name"] + '.sql', days=kwargs["days"])
            # Реузльтат SQL запроса
            result = get_info(sql)
            if not result:
                result = 'Not Found'
            return result
    elif 'number' in kwargs:
        if not kwargs["number"] or kwargs["number"].isdigit() is False:
            return "!"
        else:
            sql = provider.get(kwargs["name"] + '.sql', number=kwargs["number"])
            result = get_info(sql)
            if not result:
                result = 'Not Found'
            return result
    else:
        # Формирование выбранного SQL запроса
        sql = provider.get(kwargs["name"] + ".sql")
        # Реузльтат SQL запроса
        result = get_info(sql)
        if not result:
            result = 'Not Found'
        return result


def add_to_basket(item) -> None:
    """
    Добавление элемента в сессию (корзину)

    :param item: Элемент, добавляемый в сессию (корзину)
    :type item: tuple
    """
    basket = session.get('basket', [])  # Если корзина присутсвует в сессии
    if basket is None:
        basket = []
    basket.append(item)
    session['basket'] = basket  # Добавление элемента в сессию (корзину)


def clear_basket() -> None:
    """
    Очистка корзины и текущей цены в сессии
    """
    if 'basket' in session:
        session['basket'] = []   # Удаление корзины из сессии


def delete_from_basket(id_item: str) -> None:
    """
    Удаление выбранного элемента из корзины

    :param id_item: ID выбранного элемента в БД
    :type id_item: str
    """

    bas = session['basket']  # Получение корзины из сессии
    for i in range(len(bas)):
        # Если id выбранного элемента и id элемента в корзине совпадает
        if bas[i][0] == int(id_item):
            bas.pop(i)  # Удаление выбранного элемента из корзины
            session['basket'] = bas  # Обновление корзины
            return


def in_basket(id: str) -> bool:
    """
    Функция смотрит, существует ли в корзине добавленный элемент
    :param id:
    :return: bool
    """
    for item in session['basket']:
        if item[0] == int(id):
            return True
    return False


def pop_from_result(id_item: str, result: list) -> None:
    """
    Удаление присутсвующих элементов в корзине из общего результата

    :param id_item: ID совпадающих элементов
    :type id_item: str
    :param result: Общий результат, из которого удаляется совпадающий элемент
    :type result: list
    """

    for i in range(len(result)):
        # При совпадении переданного ID и ID элемента в результате
        if id_item == result[i][0]:
            result.pop(i)   # Удаление совпадающего элемента
            break


def in_result(result: list) -> None:
    """
    Удаляет каждый элемент корзины из результата

    :param result: Общий результат, из которого удаляются элементы корзины
    :type result: list
    """
    for item in session['basket']:
        pop_from_result(item[0], result)


def place_item(num: int):
    basket_ = session['basket']
    for item in basket_:
        if str(item[0]) == str(session['service']):
            # Добавление или изменение кол-ва товара
            if len(item) >= 6:
                basket_[basket_.index(item)][5] = int(num)
            elif len(item) == 5:
                basket_[basket_.index(item)].append(int(num))
            # Добавление или изменение общей стоимости
            if int(item[5]) >= int(item[4]):
                cost = int(item[5]) * int(item[3])
            else:
                cost = int(item[5]) * int(item[2])

            if len(item) == 6:
                basket_[basket_.index(item)].append(cost)
            elif len(item) == 7:
                basket_[basket_.index(item)][6] = cost

            session['basket'] = basket_
            return


def only():
    for item in session['basket']:
        if len(item) == 5:
            return False
    return True