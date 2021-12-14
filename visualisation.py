import datetime
import os

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
from config import PATH_TO_VIEW_FILE, PATH_TO_DAILY_REPORT_FILE_PS

st.header("Анализ данных поездок по дорогам")


@st.experimental_memo
def load_data():
    file_name = datetime.date.today().strftime('%d_%m_%y')+'.csv'
    full_path_to_save = os.path.join(PATH_TO_DAILY_REPORT_FILE_PS, file_name)
    try:
        df = pd.read_csv(full_path_to_save)
        return df
    except Exception as ex:
        print(f'возникла ошибка чтения файла {full_path_to_save}')


data = load_data()
st.header("Общее Количество Поездок за время")
years = data.index.unique()
year = st.sidebar.slider("Год", 2021, 2050)
hour = st.sidebar.slider("Шкала времени", 0, 23)

data = data[data['ЧАСЫ'] == hour]

st.markdown("Проезды между %i:00 и %i:00 " %(hour, (hour+1)))

filtered = data[
           (data['ЧАСЫ'] >= hour) & (data['ЧАСЫ'] <= (hour+1))
]

# hist = np.histogram(pd.to_datetime(filtered['Время']).dt.minute, bins=60, range=(0, 60))[0]
# chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
# fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400, )
# st.write(fig)
st.write(filtered)