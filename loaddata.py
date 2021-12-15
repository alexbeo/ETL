import datetime
import os.path
import shutil
import calendar

from config import PATH_TO_DAILY_REPORT_FILE_PS

import pandas as pd
from config import COLUMN_FOR_VIEW


class ProcessingDataFrame(object):
    def __init__(self):
        pass

    def read_from_file(self):
        pass

    def save_to_file(self):
        pass

    def clearing_dataframe(self):
        pass


class ProcessingTransactionData(object):

    def __init__(self, file_name, clear_file=True):
        self.__file_name = file_name
        self.__clear = clear_file
        if clear_file:
            self.df = self._clearing_df_for_save()
        else:
            self.df = self.read_dataframe_from_csv_file()

    def read_dataframe_from_csv_file(self):
        return pd.read_csv(self.__file_name)

    @property
    def get_columns_dataframe(self):
        return self.df.columns

    # Очистка и обработка объедененного файла ежедневных транзакций

    def _clearing_df_for_save(self, ):
        data_frame =self.read_dataframe_from_csv_file()
        data_frame = data_frame[COLUMN_FOR_VIEW]
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
        data_frame = data_frame.reindex(
            columns=['DATE', 'DAYWEEK', 'HOUR', 'MINUTE', 'SERBRTAGA', 'REGOZNIZLAZ', 'RELACIJA', 'Enter', 'VREMEULAZ',
                     'Exit', 'VREMEIZLAZ', 'IZNOSDUGUJE'])
        data_frame = data_frame.drop(['RELACIJA', 'DATE', ], axis=1)

        data_frame.columns = ['ДЕНЬ НЕДЕЛИ', 'ЧАСЫ', 'МИНУТЫ', 'ТАГ', 'ГОСНОМЕР',
                              'ВЪЕЗД', 'ВРЕМЯ ВЪЕЗДА', 'ВЫЕЗД', 'ВРЕМЯ ВЫЕЗДА', 'К ОПЛАТЕ', ]
        return data_frame

    def set_month_data(self, year, month):
        month = str(month)
        year = str(year)
        current_mes = f'{year}-{month} '
        data_frame = self.df.loc[current_mes]
        return data_frame

    @staticmethod
    def make_today_file_name():
        return datetime.date.today().strftime('%d_%m_%y') + '.csv'

    def get_enter_points(self):
        if self.__clear:
            return sorted(pd.unique(self.df['ВЪЕЗД']))
        else:
            pass

    def get_exit_points(self):
        if self.__clear:
            return sorted(pd.unique(self.df['ВЫЕЗД']))
        else:
            pass

    def aggregation_data_to_days(self,):
        if self.__clear:
            return df.groupby(df.index)['К ОПЛАТЕ'].agg(['sum', 'count',])
        else:
            pass

    # Группировка данных по дню недели сумма и количество транзакций
    def aggregation_data_to_weekdays(self):
        if self.__clear:
            return self.df.groupby(self.df['ДЕНЬ НЕДЕЛИ'])['К ОПЛАТЕ'].agg(['sum', 'count']).sort_values(by=['count'])
        else:
            pass

    def save_clear_data(self, ):
        full_path_to_save = os.path.join(PATH_TO_DAILY_REPORT_FILE_PS, self.make_today_file_name())
        self.df.to_csv(full_path_to_save, index=True)
        shutil.copy2(full_path_to_save, PATH_TO_DAILY_REPORT_FILE_PS + '/' + 'view_daily_ps.csv')


if __name__ == '__main__':

    data = ProcessingTransactionData('transformfiles/ps_daily_report/report_d_ps.csv', )
    print(data.aggregation_data_to_weekdays())

    df = data.set_month_data(2021, 12)
    sum_month = df['К ОПЛАТЕ'].sum()
    sum_transactions = df['К ОПЛАТЕ'].count()

    medium = sum_month/sum_transactions
    day_today = int(str(datetime.date.today())[-2:])-1
    day_in_month = calendar.monthrange(2021, 12)[1]
    print(f'{day_today} === {day_in_month}')
    try:
        prediction = sum_month/day_today*day_in_month
        print(
            f'ИТОГО ЗА МЕСЯЦ = {sum_month} ДИНАР   '
            f'{sum_transactions} ТРАНЗАКЦИЙ '
            f'среднее = {medium} прогноз ={prediction}')
    except Exception as ex:
        print(f'Сегодня {day_today} прогнозирование строится со 2-го дня месяца')
        print(f'{ex}')
        prediction = 0
        print(
            f'ИТОГО ЗА МЕСЯЦ = {sum_month} ДИНАР   '
            f'{sum_transactions} ТРАНЗАКЦИЙ '
            f'среднее = {medium} прогноз ={prediction}')

    print(data.aggregation_data_to_days())

    df = data.set_month_data(2021, 11)
    df_to_days = data.aggregation_data_to_days()
    df_to_days.columns = ['СУММА', "КОЛИЧЕСТВО"]
    sum = df_to_days['СУММА'].sum()
    print(df_to_days)
    print(f'Итого за месяц = {sum}')

    if data.make_today_file_name() not in os.listdir(PATH_TO_DAILY_REPORT_FILE_PS):
        data.save_clear_data()
    else:
        print(f'Файл {data.make_today_file_name()} уже сохранен в каталоге {PATH_TO_DAILY_REPORT_FILE_PS}')
