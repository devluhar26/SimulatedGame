import streamlit as st
import pandas as pd
import numpy as np
import random
from code_editor import code_editor

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
    pass

#https://docs.streamlit.io/develop/tutorials/multipage/dynamic-navigation
#
