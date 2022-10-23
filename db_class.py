from pymysql import connect, OperationalError, ProgrammingError


class UseDatabase:
    """
    Class to connect to DataBase
    """
    def __init__(self, config: dict):
        """
        Constructs all necessary attributes for class object

        :param config: Configuration dictionary for connecting to DataBase:
        {host:'host name', user:'user name', password:, database:'database name'}

        :type config: dict

        """
        self.config = config

    def __enter__(self):
        """
        Trying to connect to DataBase

        :returns:
            :return: Cursor, connected to databse
            :rtype: Class Cursor. --
            :return: Name of the error that caused the connection to the DataBase to fail
            :rtype: str

        """
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1049:
                print("Неверное название базы данных")
            if err.args[0] == 2003:
                print("Неверное имя хоста")
            return None
        except RuntimeError:
            print("Неверное имя пользователя или пароль")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closing cursor and exiting from connection to DataBase

        :param exc_type: Type of Error
        :param exc_val: Number corresponding to the error
        :type exc_type: type
        :type exc_val: int
        :returns:
            :return: True. If no fails in connecting to DataBase or exiting from Connection
            :rtype: bool
            :return String describing the error in the exit
            :rtype: str

        """
        if exc_val is None:
            self.conn.commit()
            self.conn.close()
            self.cursor.close()
        else:
            if exc_type == ProgrammingError:
                if exc_val.args[0] == 1146:
                    print('Такой таблицы не существует')
                if exc_val.args[0] == 1064:
                    print('Неправильный SQL запрос')
            elif exc_type == OperationalError:
                print('Операционная ошибка в экзите')
            else:
                print('Другая ошибка')
        return True