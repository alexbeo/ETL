import shutil
import glob
import os
import config
import pandas as pd


# Создание объединенного csv файла с нуля
def create_report_file_from_drps(path_to_reports_files, file_mask):
    list_files = glob.glob(path_to_reports_files + file_mask)
    list_files.sort()
    full_patch_to_report_file =  os.path.join(config.PATH_TO_DAILY_REPORT_FILE_PS,config.REPORT_D_PS)
    if os.path.exists(full_patch_to_report_file):
        os.remove(full_patch_to_report_file)
    with open(full_patch_to_report_file, 'wb') as file:
        for i, report_file in enumerate(list_files):
            with open(report_file, 'rb') as csv:
                if i != 0:
                    csv.readline()
                shutil.copyfileobj(csv, file)


# Ежедневное добавление нового файла в объединенный отчет
def append_daily_report_ps_file(path_today_daily_report, path_ps_daily_report, file_mask):
    try:
        today_file = glob.glob(path_today_daily_report + file_mask)[0]
        report_file = glob.glob(path_ps_daily_report + file_mask)[0]
        print(today_file, report_file)
        try:
            df1 = pd.read_csv(report_file)
            print(df1.info())
        except Exception as ex:
            print(f'Ошибка открытия файла {report_file} {ex}')
        try:
            df2 = pd.read_csv(today_file, index_col=None)
            print(df2.info())
        except Exception as ex:
            print(f'Ошибка открытия файла {report_file} {ex}')
        df3 = df1.append(df2)
        print(df3.info())
        df3.to_csv(report_file, index=False)
        os.remove(today_file)
    except Exception as ex:
        print(f'Произошла ошибка объединения файлов ежедневного отчета {ex} ')


if __name__ == '__main__':
    create_report_file_from_drps(config.DAILY_PS_TRANSACTION, '/*.csv')
    file= os.path.join(config.PATH_TO_DAILY_REPORT_FILE_PS,config.REPORT_D_PS)
    df = pd.read_csv(file)
    print(df.info())
    # append_daily_report_ps_file('inputfiles/fromps/today_tmp_report_dir','transformfiles/ps_daily_report','/*.csv')