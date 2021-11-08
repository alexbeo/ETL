import pandas as pd
from config import COLUMN_FOR_VIEW


def save_file_for_view(file_name, file_to_save):
    df = pd.read_csv(file_name, index_col=0, )
    df = df[COLUMN_FOR_VIEW]

    df['DATE'] = pd.to_datetime(df['VREME_NAPLATE'], format='%d.%m.%Y %H:%M:%S')
    df['ДАТА'] = pd.to_datetime(df['DATE'].dt.date)

    df = df.set_index('ДАТА')
    print(type(df))
    print(df.index)
    # print(df['2021-11'])
    # df = df['2021-10']
    # df = df.loc['2021-10-11':'2021-10-31']

    df['DAYWEEK'] = df['DATE'].dt.dayofweek
    df['HOUR'] = df['DATE'].dt.hour
    df['MINUTE'] = df['DATE'].dt.minute
    df = df.sort_values(by=['ДАТА', 'HOUR', 'MINUTE'])
    del(df['VREME_NAPLATE'])
    new_df = df['RELACIJA'].str.split('-', expand=True)
    new_df.columns = ['Enter', 'Exit']
    df = pd.concat([df, new_df], axis=1)
    df = df.reindex(columns=['DATE', 'DAYWEEK', 'HOUR', 'MINUTE', 'SERBRTAGA', 'REGOZNIZLAZ', 'RELACIJA', 'Enter', 'Exit', 'IZNOSDUGUJE'])
    del(df['RELACIJA'])
    del(df['DATE'])

    df.columns = ['ДЕНЬ НЕДЕЛИ', 'ЧАСЫ', 'МИНУТЫ', 'ТАГ', 'ГОСНОМЕР', 'ВЪЕЗД', 'ВЫЕЗД', 'К ОПЛАТЕ']
    df = df.loc['2021-10']
    sum = df['К ОПЛАТЕ'].sum()
    count = len(df)
    print(df.info())
    print(df.head())
    print(sum, '  ', count)
    print(pd.unique(df['ВЪЕЗД']))
    df.to_csv(file_to_save, index=True)


if __name__ == '__main__':

    save_file_for_view('transformfiles/ps_daily_report/report_d_ps.csv', 'transformfiles/ps_daily_report/view_daily_ps.csv')
    pass