import streamlit as st
import base64
def header_home():
    with open("src/ui/logo3.png", "rb") as f:
        img = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <div style='display:flex;flex-direction:column;align-items:center;justify-content:center;margin-bottom:30px;margin-top:30px'>
            <img src="data:image/png;base64,{img}" style='height:120px;border-radius:50%;'/>
            <h1 style='text-align:center;'>AttendAI</h1>
        </div>
    """, unsafe_allow_html=True)

def header_teacher():
    with open("src/ui/logo3.png", "rb") as f:
        img = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <div style='display:flex;align-items:center;justify-content:center;gap:10px;'>
            <img src="data:image/png;base64,{img}" style='height:80px;border-radius:15%;border-color:black;'/>
            <h2 style='text-align:left;font-weight:bold;color:black !important;'>AttendAI</h2>
        </div>
    """, unsafe_allow_html=True)