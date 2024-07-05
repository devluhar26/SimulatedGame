import streamlit as st
import pandas as pd
import numpy as np
import random
from code_editor import code_editor

tab1, tab2, tab3 = st.tabs(["view", "new", "modify"])

with tab1:


    st.title("simulated trading game")
    st.write("need to import table [docs.streamlit.io](https://docs.streamlit.io/).")

    import streamlit as st
    import pandas as pd

    data = {
        'strategy name': ['Strategy 1', 'Strategy 2', 'Strategy 3', 'Strategy 4', 'Strategy 5'],
        'performance': [[random.randint(0, 5000) for _ in range(30)] for _ in range(5)],
    }
    ##change the array in line 14 for the strategies true performance

    df = pd.DataFrame(data)
    event = st.dataframe(
        df,
        on_select='rerun',
        selection_mode='multi-row',
        column_config={"performance": st.column_config.LineChartColumn("performance", y_min=0, y_max=5000)},
    )

    st.button("modify")
    st.button("delete", type="primary")

with tab2:
    @st.experimental_dialog("Cast your vote")
    def logic(name):
        st.write(f"set the trading logic for {name}")
        ##add bot logic widgets here
        if st.button("add"):
            st.session_state.logic = {"name": name, }
            st.rerun()


    if "logic" not in st.session_state:
        st.title("Create a new trading strategy here")
        name = st.text_input("enter bot name here")
        if st.button("impliment"):
            logic(name)

    else:
        f"{st.session_state.logic['name']} has now been added (this is when the strat are added to sql)"

with tab3:

    response_dict = code_editor("\n\n\n\n\n\n\n\n\n\n")