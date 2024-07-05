import streamlit as st
import pandas as pd
import numpy as np

st.title("simulated trading game")
st.write("need to import table [docs.streamlit.io](https://docs.streamlit.io/).")

import streamlit as st
import pandas as pd


data = {
    'Country': ['United States', 'Canada', 'Germany', 'France', 'Japan'],
    'Capital': ['Washington, D.C.', 'Ottawa', 'Berlin', 'Paris', 'Tokyo']
}


df = pd.DataFrame(data)
st.title('Countries and Their Capitals')

event = st.dataframe(
    df,
    on_select='rerun',
    selection_mode='single-row'
)

