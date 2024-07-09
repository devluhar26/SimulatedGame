import streamlit as st
import pandas as pd
import numpy as np
import random
from code_editor import code_editor
import json
html_style_string = '''<style>
@media (min-width: 576px)
section div.block-container {
  padding-left: 20rem;
}
section div.block-container {
  padding-left: 4rem;
  padding-right: 4rem;
  max-width: 80rem;
}  

</style>'''

st.markdown(html_style_string, unsafe_allow_html=True)

#
tab1, tab2, tab3 = st.tabs(["overview", "stratgies", "something 2"])

with tab1:
    import streamlit as st
    import pandas as pd
    import numpy as np

    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    st.line_chart(chart_data)



with tab2:
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
with tab3:
    with open('user_terminal/pages/resources/example_custom_buttons_bar_adj.json') as json_button_file_alt:
        custom_buttons_alt = json.load(json_button_file_alt)

    with open('user_terminal/pages/resources/example_info_bar.json') as json_info_file:
        info_bar = json.load(json_info_file)

    height = [20, 10]
    btns = custom_buttons_alt
    st.write("Program your strategy below then Hit Save")

    response_dict = code_editor("strategy file path", height=height, buttons=btns, info=info_bar)
    if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
        code = response_dict['text']

#https://docs.streamlit.io/develop/tutorials/multipage/dynamic-navigation
#
