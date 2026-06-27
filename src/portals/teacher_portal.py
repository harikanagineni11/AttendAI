import streamlit as st
from src.components.header import header_teacher
from src.ui.style_layout import style_background_dashboard,style_layout

from src.database.db import check_teacher_exist,create_teacher,teacher_login,get_teacher_subjects

from src.components.dialog_create_subject import create_subject_dialog
from src.components.subiect_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photos import add_photos_dialog
from src.pipelines.face_pp import predict_attendance
from src.components.dialog_attendance_result import attendance_result_dialog
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.database.db import get_attendance_for_teacher
from src.components.dialog_voice_attendance import voice_attendance_dialog
def teacher_portal():
    
    style_background_dashboard()
    style_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_reg()

def teacher_dashboard():
    teacher_data=st.session_state.teacher_data
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_teacher()
    with c2:
       st.subheader(f"""Welcome,{teacher_data['name']}""")
       if st.button("Logout",type='primary',key='loginbackbtn_login',shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()
    st.space()
    
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab='take_attendance'

    tab1,tab2,tab3=st.columns(3)
    with tab1:
        type1 = "secondary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1,width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab='take_attendance'
            st.rerun()
    with tab2:
        type2 = "secondary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects',type=type2,width='stretch',icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab='manage_subjects'
            st.rerun()
    with tab3:
        type3 = "secondary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records',type=type3,width='stretch',icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab='attendance_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab=="take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab=="manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab=="attendance_records":
        teacher_tab_attendance_records()


def teacher_tab_take_attendance():
    teacher_id=st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images=[]
    subjects=get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning('You havent created any subjects yet!Please create one to begin!')
        return
    subject_option={f"{s['name']}-{s['subject_code']}":s['subject_id'] for s in subjects}
    col1,col2=st.columns([3,1],vertical_alignment='bottom')

    with col1:
        selected_sub_label=st.selectbox('Select Subject',options=list(subject_option.keys()))
    with col2:
        if (st.button('Add Photos',type='primary',icon=':material/photo_prints:',width='stretch')):
            add_photos_dialog()

    selected_sub_id=subject_option[selected_sub_label]
    st.divider()
    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols=st.columns(4)
        for idx,img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img,width='stretch',caption=f'Photo {idx+1}')
        st.divider()
        has_photos=bool(st.session_state.attendance_images)
        c1,c2,c3=st.columns(3)
        with c1:
            if st.button('Clear all photos',type='primary',width='stretch',icon=':material/delete:',disabled=not has_photos):
                st.session_state.attendance_images=[]
                st.rerun()
        with c2:
            if has_photos:
                import numpy as np
                if st.button('Run Face Analysis',type='primary',width='stretch',icon=':material/analytics:',disabled=not has_photos):
                    with st.spinner('Deep Learning classroom photos'):
                        all_detected_ids={}
                        for idx,img in enumerate(st.session_state.attendance_images):
                            img_np=np.array(img.convert('RGB'))
                            detected,_,_=predict_attendance(img_np)
                            if detected:
                                for sid in detected.keys():
                                    student_id=int(sid)
                                    all_detected_ids.setdefault(student_id,[]).append(f"Photo {idx+1}")
                        enrolled_res=supabase.table('subject_students').select("*,students(*)").eq('subject_id',selected_sub_id).execute()
                        enrolled_students=enrolled_res.data
                        if not enrolled_students:
                            st.warning('No students enrolled in this course')
                        else:
                            results,attendance_to_log=[],[]
                            current_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                            for node in enrolled_students:
                                student=node['students']
                                source=all_detected_ids.get(int(student['student_id']),[])
                                is_present=len(source)>0
                                results.append({
                                    "Name":student['name'],
                                    "ID":student['student_id'],
                                    "Source":", ".join(source) if is_present else "-",
                                    "Status":"✅ Present" if is_present else "❌ Absent"
                                })
                                attendance_to_log.append({
                                    "student_id":student['student_id'],
                                    "subject_id":selected_sub_id,
                                    "timestamp":current_timestamp,
                                    "is_present":bool(is_present)
                                })
                            attendance_result_dialog(pd.DataFrame(results),attendance_to_log)
        with c3:
            if st.button('Use Voice Attendance',type='primary',width='stretch',icon=':material/mic:'):
                voice_attendance_dialog(selected_sub_id)




def teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data['teacher_id']
    col1,col2=st.columns(2)
    with col1:
        st.header('Manage subjects',width='stretch')
    with col2:
       if st.button('Create New subject',width='stretch'):
           create_subject_dialog(teacher_id)
    #LIST OF ALL SUBJECTS
    subjects=get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats=[
                ("🫂","Students",sub['total_students']),
                ("🕰️","Classes",sub['total_classes'])
            ]
            def share_btn():
                if st.button(f"""Share Code:{sub['name']}""",key=f"""share_{sub['subject_code']}""",icon=':material/share:'):
                    share_subject_dialog(sub['name'],sub['subject_code'])

                st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECT FOUND.CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header('Attendance Records')
    teacher_id=st.session_state.teacher_data['teacher_id']
    records=get_attendance_for_teacher(teacher_id)
    if not records:
        return
    data=[]
    for r in records:
        ts=r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject": r['subject']['name'],
            "Subject Code":r['subject']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })
    df=pd.DataFrame(data)

    summary=(
        df.groupby(['ts_group','Time','Subject','Subject Code'])
        .agg(
            Present_count=('is_present','sum'),
            Total_count=('is_present','count')
        ).reset_index()
    )
    summary['Attendance Stats']=(
        "✅"+summary['Present_count'].astype(str)+" /"
        +summary['Total_count'].astype(str)+' Students'
    )
    display_df=(summary.sort_values(by='ts_group',ascending=False)
                [['Time','Subject','Subject Code','Attendance Stats']]
                )
    st.dataframe(display_df,width='stretch',hide_index=True)




def login_teacher(teacher_uname,teacher_pass):
    if not teacher_uname or not teacher_pass:
        return False
    teacher=teacher_login(teacher_uname,teacher_pass)
    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    return False

def teacher_screen_login():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_teacher()
    with c2:
       if st.button("Go back to Home",type='primary',key='loginbackbtn_login',shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()
    
    st.header("Login using password",text_alignment='center')

    st.space()
    st.space()
    teacher_uname=st.text_input("Enter username",placeholder='abhishek')
    teacher_pass=st.text_input("Enter password",type='password',placeholder='Enter password')

    st.divider()
    btnc1,btnc2=st.columns(2)
    with btnc1:
        if st.button("Login",type='primary',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            if login_teacher(teacher_uname,teacher_pass):
                st.toast("Welcome back!")
                import time
                time.sleep(1)
                st.rerun()
            else :
                st.error("Invalid username or password")

    with btnc2:
       if st.button("Register instead",type='secondary',icon=':material/passkey:',width='stretch'):
           st.session_state.teacher_login_type='register'
           st.rerun()
            
def register_teacher(teacher_uname,teacher_name,teacher_pass,teacher_pass_confirm):
    if not teacher_uname or not teacher_name or not teacher_pass :
        return False,"All Fields are required!"
    if check_teacher_exist(teacher_uname):
        return  False,"Username already Exists"
    if teacher_pass != teacher_pass_confirm:
        return False,"Password doesn't match"
    try:
        create_teacher(teacher_uname,teacher_pass,teacher_name)
        return True,"Successfully Created!Login now"
    except Exception as e:
        print(e)
        return False,"Unexpected error!"

def teacher_screen_reg():
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_teacher()
    with c2:
        if st.button("Go back to Home",type='primary',key='loginbackbtn_reg',shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()
    
    st.header("Register Your teacher profile",text_alignment='center')

    st.space()
    st.space()
    teacher_uname=st.text_input("Enter username",placeholder='abhishek')
    teacher_name=st.text_input("Enter FullName",placeholder='abhishek daggubati')
    teacher_pass=st.text_input("Enter password",type='password',placeholder='Enter password')
    teacher_pass_confirm=st.text_input("Confirm password",type='password',placeholder='Confirm password')
    st.divider()
    btnc1,btnc2=st.columns(2)
    with btnc1:
       if st.button("Register now",type='primary',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            success,message=register_teacher(teacher_uname,teacher_name,teacher_pass,teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type='login'
                st.rerun()
            else :
                st.error(message)
    with btnc2:
        if st.button("Login instead",type='secondary',icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type='login'
            st.rerun()   