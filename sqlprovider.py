import os
from string import Template


class SQLProvider:
    def __init__(self, file_path: str) -> None:
        """
        Constructs all necessary attributes for class object

        :param file_path: File path to directory with SQL files
        :type file_path: str
        """
        self._scripts={}
        for file in os.listdir(file_path):  #file_path - путь до папки sql
            self._scripts[file]=Template(open(f'{file_path}/{file}', 'r').read())

    def get(self,name,**kwargs):  #get('avto_by_lift.sql', lift=...
        """
        Creates a sql query with the values of the passed arguments (if any)

        :param name: Name of SQL script file
        :param kwargs: Any. Arguments used in sql scripts
        :type name: str
        :type kwargs: int, float, str§§

        :return: String SQL inquiry
        :rtype: str

        """
        return self._scripts[name].substitute(**kwargs)

