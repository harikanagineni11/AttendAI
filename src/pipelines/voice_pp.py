import streamlit as st
import librosa
import numpy as np
import io
import resemblyzer
print("ok..r")
from resemblyzer import preprocess_wav
print("ok..preprocess")


@st.cache_resource
def load_voice_encoder():
    try:
        from resemblyzer import VoiceEncoder
        print("Loading VoiceEncoder...")
        encoder = VoiceEncoder()
        print("VoiceEncoder loaded")
        return encoder
    except Exception as e:
        print("VoiceEncoder error:", e)
        raise



def get_voice_embedding(audio_bytes):
    try:
        
        encoder=load_voice_encoder()
        audio,sr=librosa.load(io.BytesIO(audio_bytes),sr=16000)
        wav=preprocess_wav(audio)
        embedding=encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error(f"Voice recog error: {e}")
        print("Voice recog error:", e)
        return None
    
def identify_speaker(new_embedding,candidates_dict,threshold=0.65):
    if new_embedding is None or not candidates_dict:
        return None,0.0
    best_sid=None
    best_score=-1.0
    for sid,stored_embedding in candidates_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding) / (
                np.linalg.norm(new_embedding) *
                np.linalg.norm(stored_embedding)
            )
            if similarity>best_score:
                best_score=similarity
                best_sid=sid
    if best_score>=threshold:
        return best_sid,best_score
    return None,best_score

def process_bulk_audio(audio_bytes,candidates_dict,threshold=0.65):
    try:
        encoder=load_voice_encoder()
        audio,sr=librosa.load(io.BytesIO(audio_bytes),sr=16000)
        segments=librosa.effects.split(audio,top_db=30)
        
        identified_res={}
        for start,end in segments:
            if (end-start)<sr*0.5:
                continue
            segment_audio=audio[start:end]
            wav=preprocess_wav(segment_audio)
            embedding=encoder.embed_utterance(wav)
            sid,score=identify_speaker(embedding,candidates_dict,threshold)
            if sid:
                if sid not in identified_res or score>identified_res[sid]:
                    identified_res[sid]=score
        return identified_res
    except Exception as e:
        st.error(f"Bulk Process error: {e}")
        print("Bulk Process error:", e)
        return {}