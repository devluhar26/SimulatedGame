import streamlit as st
import pandas as pd
import numpy as np
import random
st.title("simulated trading game")
st.write("need to import table [docs.streamlit.io](https://docs.streamlit.io/).")

import streamlit as st
import pandas as pd


data = {
    'strategy name': ['United States', 'Canada', 'Germany', 'France', 'Japan'],
    'performance':  [[random.randint(0, 5000) for _ in range(30)] for _ in range(5)],
}


df = pd.DataFrame(data)
event = st.dataframe(
    df,
    on_select='rerun',
    selection_mode='single-row',
    column_config={"performance":st.column_config.LineChartColumn("performance", y_min=0, y_max=5000)},
)

