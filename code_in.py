# Функция шифрвания данных пользователя
def user_code(string: str):
    """
    Encrypts the input string and returns it

    Args:
        string: str. An input string
    Return:
        str. Encrypts string
    """
    final = ''
    # Проход по каждому элементу строки
    for x in string:
        # Если это буква, это заглавная буква, то она заменяется на утроенные строчные,
        # если строчная - на удвоенные заглавные
        if x.isalpha() is True:
            if x.isupper() is True:
                x = x.lower()
                x = x*3
            else:
                x = x.upper()
                x = x*2
        # Если это цифра, то 0 заменяется на 1, а остальные на количество 0, соответсвующее значению 0
        if x.isdigit() is True:
            if x == 0:
                x = '1'
            else:
                x = "0"*int(x)
        final += x
    return final


