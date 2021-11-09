import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
from config import PATH_TO_VIEW_FILE

st.header("Анализ данных поездок по дорогам")


@st.experimental_memo
def load_data():
    df = pd.read_csv(PATH_TO_VIEW_FILE)
    return df


data = load_data()
st.header("Общее Количество Поездок за время")
hour = st.sidebar.slider("Шкала времени", 0, 23)
data = data[data['Время'] == hour]

st.markdown("Проезды между %i:00 и %i:00 " %(hour, (hour+1)))

filtered = data[
           (data['Время'] >= hour) & (data['Время'] <= (hour+1))
]

# hist = np.histogram(pd.to_datetime(filtered['Время']).dt.minute, bins=60, range=(0, 60))[0]
# chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
# fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400, )
# st.write(fig)
st.write(filtered)