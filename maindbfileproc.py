import pandas as pd

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




if __name__ == '__main__':
    tfp1 = TagFileProcessing(FULL_PATH_TO_FILE)

    # print(df.df.head())
    # print(df.df.columns)
    print(tfp1.df.to_markdown())
    # list_TAGs = list(tfp1.main_df.TAGid)
    # print(len(list_TAGs))
    # print(len(set(list_TAGs)))

    # def condition(df):
    #     if df['Point'] == 'Брак/возврат':
    #         return 'Return'
    #
    # tfp1.main_df['TAG_CONDITION'] = tfp1.main_df.apply(condition, axis=1)
    #
    # df = tfp1.main_df.reindex( columns = ['id', 'TAGid', 'Date input', 'TMP1', 'TAG_CONDITION', 'Date output',
    #                                                                 'Point', 'TMP2', 'Date activation',
    #                         'Num Contract', 'Client', 'Category', 'Car number', 'Card mask', 'Card Blocked',
    #                         'OBU Blocked', 'CID', 'Stop lists', 'Comment', 'TMP3', 'TMP4', 'TMP5', 'TMP6'])
    # new_df = df[(tfp1.main_df['Point'] == 'Брак/возврат')]
    # print(df.to_markdown())
