import datetime
import streamlit as st

d = st.date_input("When's your birthday", datetime.date(2019, 7, 6))
st.write("Your birthday is:", d)
st.divider()

st.button("Reset", type="primary")
if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")
st.divider()

left, middle = st.columns(2)
if left.button("Plain button", use_container_width=True):
    left.markdown("You clicked the plain button.")
if middle.button("Emoji button", use_container_width=True):
    middle.markdown("You clicked the emoji button.")