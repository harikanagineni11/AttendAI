import streamlit as st
import pandas as pd
import numpy as np
from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    import dlib
    import numpy as np
    import face_recognition_models
    
    detector=dlib.get_frontal_face_detector()
    sp=dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    face_rec=dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector,sp,face_rec
@st.cache_resource
def get_face_embeddings(image_np):
    detector,sp,face_rec=load_dlib_models()
    faces=detector(image_np,1)

    encodings=[]
    for face in faces:
        shape=sp(image_np,face)
        face_descriptor=face_rec.compute_face_descriptor(image_np,shape,1) #128 embeddings come

        encodings.append(np.array(face_descriptor))
    return encodings

def get_trained_model():
    X=[] #embeddngs
    y=[] #ids
    std_db=get_all_students()
    if not std_db:
        return None
    for std in std_db:
        embedding=std.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(std.get('student_id'))

    if(len(X)==0):
        return 0
    from sklearn.svm import SVC
    clf=SVC(kernel='linear',probability=True,class_weight='balanced')
    try:
        clf.fit(X,y)
    except ValueError:
        pass
    return {'clf':clf,'X':X,'y':y}

def train_classifier():
    st.cache_resource.clear()
    model_data=get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings=get_face_embeddings(class_image_np)
    detected_student={}
    model_data=get_trained_model()

    if not model_data:
        return detected_student,[],len(encodings)
    clf=model_data['clf']
    X_train=model_data['X']
    y_train=model_data['y']
    all_students=sorted(list(set(y_train)))

    for encoding in encodings:
        if len(all_students)>=2:
            predicted_id=int(clf.predict([encoding])[0])
        else:
            predicted_id=int(all_students[0])
        student_embedding=X_train[y_train.index(predicted_id)]
        best_match_score=np.linalg.norm(student_embedding-encoding)
        resemblance_threshold=0.6
        if best_match_score<=resemblance_threshold:
            detected_student[predicted_id]=True
    return detected_student,all_students,len(encodings)