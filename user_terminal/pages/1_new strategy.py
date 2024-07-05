import streamlit as st



tab1, tab2, tab3 = st.tabs(["view", "new", "modify"])

with tab1:
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

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)