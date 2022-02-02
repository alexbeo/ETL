import pandas as pd
import datetime

FULL_PATH_TO_FILE = 'inputfiles/fromoffice/ТАГИ 2021_12_15.xlsx'


class TagFileProcessing:
    TAG_CONDITION = ['ISSUED', 'NOT ISSUED', 'RETURN']
    TAG_STATUS = ['ACTIVE', 'BLOCKED']
    NEW_TABLE_COL = ['id', 'TAGid', 'Date input', 'TMP1', 'Date output', 'Point', 'TMP2', 'Date activation',
                     'Num Contract', 'Client', 'Category', 'Car number', 'Card mask', 'Card Blocked',
                     'OBU Blocked', 'CID', 'Stop lists', 'Comment', 'TMP3', 'TMP4', 'TMP5', 'TMP6']

    def __init__(self, input_file):
        self.__data_frame = self.read_from_file(input_file)
        self.__data_frame.columns = self.NEW_TABLE_COL

    @property
    def df(self):
        return self.__data_frame

    @df.setter
    def df(self, data_frame):
        self.__data_frame = data_frame

    @property
    def column(self):
        return self.__data_frame.columns

    @column.setter
    def column(self, col_list):
        if len(self.__data_frame.columns) != len(col_list):
            raise ValueError(f'Количество столбцов не может отличатся от первончального {len(self.__data_frame.columns)}')
        self.__data_frame.columns = col_list

    @classmethod
    def read_from_file(cls, input_file):
        return pd.read_excel(input_file, 'Основной', skiprows=1, engine='openpyxl')


class TAG:

    _status = ('Warehouse', 'Active', 'Blocked', 'Return')
    _id = 0
    count = 0

    def __init__(self, tag_id, date=datetime.datetime.today().date()):
        TAG.count += 1
        self.__id = self._validate_tag_id(tag_id)
        if self._id == 0:
            self.__status = self._status[0]
        else:
            self.__status = self.status
        self.__cid = ''

        self.__date_in = date

    def _validate_tag_id(self, tag_id):
        if isinstance(tag_id, int):
            if len(str(tag_id)) == 11:
                return tag_id
            else:
                raise ValueError('Длина номера тага должна иметь не менее 11 чисел')
        else:
            raise TypeError('Номер тага должен быть целым числом')

    @property
    def id(self):
        return self.__id

    def _validate_status(self, status_id):
        if isinstance(status_id, int):
            if -1 < status_id < 5:
                return True
            else:
                raise ValueError('Значение статуса ТАГа вышло за границу диапазона 1..4')
        else:
            raise TypeError('Статус ТАГа это целое число')

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, num_status):
        if self._validate_status(num_status):
            self.__status = self._status[num_status]

    def add_to_db(self):
        pass

    def del_from_db(self):
        pass

    def __str__(self):
        return f'Номер ТАГа: {self.__id} Дата поступления на склад: {self.__date_in} Статус тага: {self.__status}'


if __name__ == '__main__':
    tag1 = TAG(11111111111)
    tag2 = TAG(21111111111)
    tag3 = TAG(21111111111)
    print(tag1, tag2, tag3)

    print(TAG.__dict__)