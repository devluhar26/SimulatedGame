import streamlit as st
import pandas as pd
import numpy as np
import random
from code_editor import code_editor
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
.floating-side-bar {
    display: flex;
    flex-direction: column;
    position: fixed;
    margin-top: 2rem;
    margin-left: 2.75rem;
    margin-right: 2.75rem;
}
.flt-bar-hd {
    color: #5e6572;
    margin: 1rem 0.1rem 0 0;
}
.floating-side-bar a {
    color: #b3b8c2;

}
.floating-side-bar a:hover {

}
.floating-side-bar a.l2 {

}
</style>'''

st.markdown(html_style_string, unsafe_allow_html=True)

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
