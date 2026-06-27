import streamlit as st


from src.portals.home_screen import home_screen
from src.portals.teacher_portal import teacher_portal
from src.portals.student_portal import student_portal
from src.components.dialog_auto_enroll import auto_enroll_dialog
from PIL import Image


def main():
    logo = Image.open("src/ui/logo3.png")
    st.set_page_config(
        page_title='AttendAI-Making Attendance faster using AI',
        page_icon=logo
    )
    if 'login_type' not in st.session_state:
        st.session_state["login_type"]=None
    match st.session_state['login_type']:
        case 'teacher':
            teacher_portal()
        case 'student':
            student_portal()
        case None:
            home_screen()

    join_code=st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type !='student':
            st.session_state.login_type='student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role')=='student':
            auto_enroll_dialog(join_code)
main()