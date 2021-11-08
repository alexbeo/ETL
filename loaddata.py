import pandas as pd
from config import COLUMN_FOR_VIEW


def save_file_for_view(file_name, file_to_save):
    df = pd.read_csv(file_name, index_col=0)
    df = df[COLUMN_FOR_VIEW]
    df['DATE'] = pd.to_datetime(df['VREME_NAPLATE'])
    df['DAY'] = df['DATE'].dt.date
    df['HOUR'] = df['DATE'].dt.hour
    df['MINUTE'] = df['DATE'].dt.minute
    del(df['VREME_NAPLATE'])
    del(df['DATE'])
    df.columns = ['Номер машины', 'Участок', 'Цена проезда', 'TAGID', 'Дата', 'Часы', 'Минуты']
    print(df.info())
    print(df.head())
    df.to_csv(file_to_save, index=False)


if __name__ == '__main__':

    save_file_for_view('transformfiles/ps_daily_report/report_d_ps.csv', 'transformfiles/ps_daily_report/view_daily_ps.csv')
    pass