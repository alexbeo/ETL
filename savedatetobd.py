import datetime
import os.path
import shutil
import calendar

from config import PATH_TO_DAILY_REPORT_FILE_PS

import pandas as pd
from config import COLUMN_FOR_VIEW

FULL_PATH_TO_FILE = 'transformfiles/ps_daily_report/report_d_ps.csv'
FULL_PATH_TO_SAVE = 'transformfiles/ps_daily_report/report_d_ps_1.csv'


class TransactionProcessing:

    in_col = ['DATE', 'DAYWEEK', 'HOUR', 'MINUTE', 'SERBRTAGA', 'REGOZNIZLAZ', 'RELACIJA', 'Enter', 'VREMEULAZ', 'Exit',
           'VREMEIZLAZ', 'IZNOSDUGUJE']
    del_col = ['RELACIJA', 'DATE', ]
    set_col = ['ДЕНЬ НЕДЕЛИ', 'ЧАСЫ', 'МИНУТЫ', 'ТАГ', 'ГОСНОМЕР', 'ВЪЕЗД', 'ВРЕМЯ ВЪЕЗДА', 'ВЫЕЗД', 'ВРЕМЯ ВЫЕЗДА',
               'К ОПЛАТЕ', ]

    def __init__(self, input_file):
        self.__input_file = input_file
        self.__dirty_df = self.read_from_csv_file(self.__input_file)
        self.__columns = self.__dirty_df.columns
        self.__clear_df = self.clearing_dataframe(self.__dirty_df)

    @property
    def columns(self):
        return self.__clear_df.columns

    @classmethod
    def read_from_csv_file(cls, input_file):
        return pd.read_csv(input_file)

    @staticmethod
    def save_file_to_csv(data_frame, full_file_path):
        data_frame.to_csv(full_file_path)

    @staticmethod
    def delete_columns(data_frame, *args):
        return data_frame.drop(*args, axis=1)

    @staticmethod
    def reindex_column(data_frame, columns):
        data_frame = data_frame.reindex(columns=columns)

    def month_data(self, year, month):
        month = str(month)
        year = str(year)
        current_mes = f'{year}-{month} '
        return self.__clear_df.loc[current_mes]

    def daily_data_agg(self, year, month):
        data_frame = self.month_data(year, month)
        data_frame = data_frame.groupby(data_frame.index)['К ОПЛАТЕ'].agg(['sum', 'count'])
        data_frame.columns = ['СУММА', 'КОЛИЧЕСТВО']
        return data_frame

    def month_data_agg(self, year, list_month):
        data_frame = self.daily_data_agg(year, list_month[0])
        for month in list_month:
            if month < 12:
                data_frame = data_frame.append(self.daily_data_agg(year, month+1))
        return data_frame

    def one_month_sum(self, year, month):
        data_frame = self.daily_data_agg(year, month)
        sum_operation = data_frame['СУММА'].sum()
        day_count = data_frame['СУММА'].count()
        medium = float(sum_operation)/float(day_count)
        count_operation = self.month_data(year, month)['К ОПЛАТЕ'].count()
        return sum_operation, count_operation, medium

    @classmethod
    def clearing_dataframe(cls, data_frame):
        data_frame = data_frame[COLUMN_FOR_VIEW].copy()
        data_frame['DATE'] = pd.to_datetime(data_frame['VREME_NAPLATE'], format='%d.%m.%Y %H:%M:%S')
        data_frame['VREMEULAZ'] = pd.to_datetime(data_frame['VREMEULAZ'], infer_datetime_format=True, )
        data_frame['VREMEIZLAZ'] = pd.to_datetime(data_frame['VREMEIZLAZ'], infer_datetime_format=True)
        data_frame['ДАТА'] = pd.to_datetime(data_frame['DATE'].dt.date)
        data_frame = data_frame.set_index('ДАТА')
        data_frame['DAYWEEK'] = data_frame['DATE'].dt.dayofweek
        data_frame['HOUR'] = data_frame['DATE'].dt.hour
        data_frame['MINUTE'] = data_frame['DATE'].dt.minute
        data_frame = data_frame.sort_values(by=['ДАТА', 'HOUR', 'MINUTE'])
        del (data_frame['VREME_NAPLATE'])
        new_df = data_frame['RELACIJA'].str.split('-', expand=True)
        new_df.columns = ['Enter', 'Exit']
        new_df['Enter'] = new_df['Enter'].str[:-1]
        new_df['Exit'] = new_df['Exit'].str[1:]
        data_frame = pd.concat([data_frame, new_df], axis=1)
        data_frame = data_frame.reindex(columns=cls.in_col)
        data_frame = cls.delete_columns(data_frame, cls.del_col)
        data_frame.columns = cls.set_col
        return data_frame



if __name__ == '__main__':

    df =TransactionProcessing(FULL_PATH_TO_FILE)



    # print(df.month_data(2021, 12).info())
    print(df.daily_data_agg(2021, 12).to_markdown())
    # print(df.month_data_agg(2021, (10, 11, 12)).to_markdown())
    summa, count, medium = df.one_month_sum(2021,12)
    print(f'ИТОГО С НАЧАЛА МЕСЯЦА ВЫРУЧКА = {summa:,.0f}, КОЛИЧЕСТВО ТРАНЗАКЦИЙ = {count}, СРЕДНЕЕ ЗА ДЕНЬ = {medium:,.0f}')





