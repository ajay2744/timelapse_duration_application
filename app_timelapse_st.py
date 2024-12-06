import streamlit as st
import cv2
import tempfile
import os
import matplotlib.pyplot as plt
import numpy as np


    
def bright_percent_pixel(frame):
    frame_hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    s=frame_hsv[:,:,1]
    v=frame_hsv[:,:,2]

    s_th=80
    v_th=80

    mask=(s>s_th) & (v>v_th)

    return np.sum(mask)*100/mask.size

def day_night_evening_percent(timelapse_file_path):
    
    cap=cv2.VideoCapture(timelapse_file_path)
    day_frames_count=0
    night_frames_count=0
    evening_frames_count=0
    while True:
        ret,frame=cap.read()
        if not ret:
            print("Frames not present or ended")
            break
        
        
            #cv2.imshow('w',frame)
        if bright_percent_pixel(frame)<10:
            night_frames_count+=1
        elif bright_percent_pixel(frame)<30:
            evening_frames_count+=1
        else:
            day_frames_count+=1
    total_frames=day_frames_count+night_frames_count+evening_frames_count
    day_frames_percent=day_frames_count*100/total_frames
    night_frames_percent=night_frames_count*100/total_frames
    evening_frames_percent=evening_frames_count*100/total_frames


    fig,ax=plt.subplots()
    labels=['DAY','NIGHT','EVENING/EARLY MORNING']
    sizes=[day_frames_percent,night_frames_percent,evening_frames_percent]
    ax.pie(sizes,labels=labels,autopct="%1.1f%%")

    st.pyplot(fig)

st.title("welcome")

uploaded_video=st.file_uploader("Upload time lapse file",type=['mp4'])


if uploaded_video is not None:
    st.video(uploaded_video)
    temp_dir=tempfile.TemporaryDirectory()
    
    video_path=os.path.join(temp_dir.name,uploaded_video.name)

    with open(video_path,"wb") as f:
        f.write(uploaded_video.read())

    day_night_evening_percent(video_path)
    temp_dir.cleanup()


    

