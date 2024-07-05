import streamlit as st
import pandas as pd
import numpy as np

st.title("simulated trading game")
st.write("need to import table [docs.streamlit.io](https://docs.streamlit.io/).")


df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))

st.dataframe(df)  # Same as st.write(df)