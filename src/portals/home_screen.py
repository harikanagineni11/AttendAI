import streamlit as st
import base64
from src.components.header import header_home
from src.ui.style_layout import style_layout,style_background_home
def home_screen():
    
    header_home()
    
    style_layout()
    style_background_home()
    col1,col2=st.columns(2,gap="large")
    with col1:
        st.header("I'm Student")
        st.image("src/ui/student1.png",width=120)
        if st.button('Student Portal',type='primary',icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type']='student'
            st.rerun()
    with col2:
        st.header("I'm Teacher")
        st.image("src/ui/Teacher1.png",width=120)
        if st.button('Teacher Portal',type='primary',icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type']='teacher'
            st.rerun()
        