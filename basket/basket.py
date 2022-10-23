from flask import Blueprint, render_template, request, session, redirect

from in_db import clear_basket, delete_from_basket, \
    get_info, add_to_basket, use_roots, in_result, place_item, only
from sqlprovider import SQLProvider

provider = SQLProvider('/Users/elizavetacernyseva/PycharmProjects/kursovaya/basket/sql')

basket_app = Blueprint('basket', __name__, template_folder='templates')


@basket_app.route('/')
@use_roots
def intro():
    return render_template('basket_intro.html')


@basket_app.route('/basket_', methods=['POST', 'GET'])
@use_roots
def basket_():
    if request.method == 'GET':
        session['basket'] = []  # Очистка корзины
        sql = provider.get('all_postovchiki.sql')  # Получение данных о поставщиках
        result = get_info(sql)
        return render_template('all.html', items=result)
    else:
        item_id = request.form.get('item_id')   # Получение id выбранного поставщика
        session['id'] = item_id
        return redirect('/basket/basket_buy')


@basket_app.route('/basket_buy', methods=['POST', 'GET'])
@use_roots
def basket_buy():
    if request.method == 'GET':
        # Получение данных об услугах, предоставляемых выбранным поставщиком
        sql = provider.get('order_list.sql', id=session['id'])
        result = list(get_info(sql))
        in_result(result)   # Удаляем из списка предоставляемых услуг, услуги находящиеся в корзине
        return render_template('basket_order_list.html', items=result,
                               basket=session['basket'])
    else:
        item_id = request.form.get('item_id')
        if request.form.get("btn") == "Удалить":  # Удаление из корзины
            delete_from_basket(item_id)
        elif request.form.get("enter") == "Ввести количество":
            session['service'] = item_id    # Занесение в сессию id выбранной услуги
            return redirect('/basket/enter_num')
        else:
            sql = provider.get('order_item.sql', id=item_id)    # Получение данных о выбранной услуге
            items = get_info(sql)
            # Добавление в корзину полученных данных
            add_to_basket(list(items[0]))
        return redirect('/basket/basket_buy')


@basket_app.route('/enter_num', methods=['POST', 'GET'])
@use_roots
def enter_num():
    if request.method == "GET":
        # Получение данных об услуге и товаре
        item = get_info(provider.get('item.sql', id=session['service']))[0]
        return render_template('enter_num.html', item=item)
    else:
        # Добавляем/меняем количество и стоимость товара в корзине
        col = request.form.get("num")
        if col.isdigit() is True:
            place_item(col)
        else:
            item = get_info(provider.get('item.sql', id=session['service']))[0]
            return render_template('enter_num.html', item=item, title="Введите число")
        return redirect('/basket/basket_buy')


@basket_app.route('/clear')
@use_roots
def clear_basket_handler():
    """
    Функция очистки корзины
    """
    clear_basket()
    return redirect('/basket/basket_buy')


@basket_app.route('/buy')
@use_roots
def buy_items():
    if only() is False:
        return redirect('/basket/basket_buy')
    _basket = session.get('basket')
    for item in _basket:
        # Получение длительности поставки для для текущей услуги
        sql = provider.get('duration_post.sql', id=item[0])
        dur = int(get_info(sql)[0][0])
        # Определение цены, в зависимости от кол-ва товара
        cost = item[2]
        if int(item[5]) >= int(item[4]):
            cost = item[3]
        # Занесение в бд всех данных о текущей поставке
        sql = provider.get('insert_postavka.sql', id=item[0], price=cost,
                           col_vo=item[5], date=dur)
        get_info(sql)
        # Получение id заказанного товара
        sql = provider.get('get_id.sql', id=item[0])
        id_item = get_info(sql)[0][0]
        # Получение кол-ва товара на складе
        sql = provider.get('get_num_tovar.sql', id=id_item)
        num = int(get_info(sql)[0][0])
        # Обновление информации о товаре на складе
        sql = provider.get('update_sklad.sql', id=id_item, n=num + int(item[5]))
        get_info(sql)
    clear_basket()  # Очистка корзины
    return redirect('/basket')
