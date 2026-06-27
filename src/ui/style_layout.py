import streamlit as st


#styles for home screen
def style_background_home():
    st.markdown("""
        <style>
            .stApp{
                background:#9370DB !important; 
                }
            div[data-testid="stColumn"]{
                background:#FFF6F6 !important;
                border-radius:5rem;
                padding:2.3rem !important;
                transition: transform 0.2s ease-in-out,
                box-shadow 0.2s ease-in-out !important;
            }
            div[data-testid="stColumn"]:hover{
                transform: scale(1.0);
                box-shadow: 0 12px 25px rgba(0,0,0,0.15);
            }
            div[data-testid="stColumn"] h1,
            div[data-testid="stColumn"] h2,
            div[data-testid="stColumn"] h3{
                color:black !important;
            }
        </style>
""",unsafe_allow_html=True)
    
def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp{
                background:#e4cef0 !important; 
                }
            div[data-testid="stHeadingWithActionElements"] h2{
                color:black !important;
            }
            div[data-testid="stHeadingWithActionElements"] p{
                font-weight:bold !important;
            }
        </style>
""",unsafe_allow_html=True)    
    
def style_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Aladin&family=Berkshire+Swash&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Elms+Sans:ital,wght@0,100..900;1,100..900&display=swap');

        #MainMenu, footer, header {
            visibility: hidden;
        }
        .block-container {
            padding-top: 1.5rem !important;
        }

        /* Target headings via Streamlit's markdown wrapper, not bare tags */
        div[data-testid="stMarkdownContainer"] h1
        {
            font-family: "Aladin", system-ui !important;
            font-size: 3.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
            color: #F5F5F5;
        }
        div[data-testid="stMarkdownContainer"]
        h2 {
            font-family: "Aladin", system-ui !important;
            font-size: 2rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
            color: #F5F5F5;
        }
        div[data-testid="stMarkdownContainer"] h3,
        div[data-testid="stMarkdownContainer"] h4,
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] span {
            font-family: "Elms Sans", sans-serif !important;
        }

        /* Target Streamlit's actual button structure */
        div[data-testid="stButton"] button,
        .stButton > button {
            border-radius: 1.5rem !important;
            background: #EB459E !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }
        div[data-testid="stButton"] button[kind="secondary"],
        .stButton > button[kind="secondary"] {
            border-radius: 1.5rem !important;
            background: #5865F2!important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }
        div[data-testid="stButton"] button:hover,
        .stButton > button:hover {
            transform: scale(1.05) !important;
        }
        div[data-testid="stButton"] button[kind="tertiary"],
        .stButton > button[kind="tertiary"] {
            border-radius: 1.5rem !important;
            background: black !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
        }
        </style>
    """, unsafe_allow_html=True)

 
   