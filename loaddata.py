import pandas as pd
from config import COLUMN_FOR_VIEW


def save_file_for_view(file_name, file_to_save):
    df = pd.read_csv(file_name)
    df = df[COLUMN_FOR_VIEW]
    df['DATE'] = pd.to_datetime(df['VREMEIZLAZ']).dt.date
    df['TIME'] = pd.to_datetime(df['VREMEIZLAZ']).dt.hour
    del(df['VREMEIZLAZ'])
    df.columns = ['Номер машины', 'Участок', 'Цена проезда', 'TAGID', 'Дата', 'Время']
    print(df.info())
    print(df.head())
    df.to_csv(file_to_save, index=False)


if __name__ == '__main__':

    save_file_for_view('transformfiles/ps_daily_report/report_d_ps.csv', 'transformfiles/ps_daily_report/view_daily_ps.csv')
    pass