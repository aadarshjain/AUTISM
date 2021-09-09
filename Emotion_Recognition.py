
# -*- coding: utf-8 -*-
"""
Emotion Recognition
"""
import sqlite3 

#import cv2
import time
import numpy as np
import cv2
from keras.models import load_model
import h5py

############################################################
def counting(emotionlist,username):
    AngryCount=0
    DisgustCount=0
    FearCount=0
    HappyCount=0
    SadCount=0
    SurpriseCount=0
    NeutralCount=0
    for i in emotionlist:
        if i == 'Angry':
            AngryCount = AngryCount + 1
        elif i == 'Disgust':
            DisgustCount = DisgustCount + 1
        elif i == 'Fear':
            FearCount = FearCount + 1
        elif i == 'Happy':
            HappyCount = HappyCount + 1
        elif i == 'Sad':
            SadCount = SadCount + 1
        elif i == 'Surprise':
            SurpriseCount = SurpriseCount + 1
        else :
            NeutralCount = NeutralCount + 1
            
    emotionCount = [AngryCount,DisgustCount,FearCount,HappyCount,SadCount,SurpriseCount,NeutralCount]
    print(emotionCount)
    with sqlite3.connect("database.db") as con:  
                cur = con.cursor() 
                cur.execute("""UPDATE AUTISM SET
	ANGRYCOUNT={},DISGUSTCOUNT={},FEARCOUNT={},HAPPYCOUNT={},SADCOUNT={},SURPRISECOUNT={},NEUTRALCOUNT={} 
	WHERE USERNAME=username """.format(emotionCount[0],emotionCount[1],emotionCount[2],emotionCount[3],
		emotionCount[4],emotionCount[5],emotionCount[6]))


                #cur.execute("""UPDATE DATABASE SET (AGE,ID1,ID2,ANGRYCOUNT,DISGUSTCOUNT,FEARCOUNT,HAPPYCOUNT,SADCOUNT,SURPRISECOUNT,NEUTRALCOUNT,
                #TEMPERATURE,HEARTRATE,POSITIVE_EMOTIONS,NEGATIVE_EMOTIONS) = (SELECT AUTISM.AGE,AUTISM.ID4,AUTISM.ID5,AUTISM.ANGRYCOUNT,
                #AUTISM.DISGUSTCOUNT,AUTISM.FEARCOUNT,AUTISM.HAPPYCOUNT,AUTISM.SADCOUNT,AUTISM.SURPRISECOUNT,AUTISM.NEUTRALCOUNT,AUTISM.TEMPERATURE,
                #AUTISM.HEARTRATE,(AUTISM.HAPPYCOUNT+AUTISM.NEUTRALCOUNT+AUTISM.SURPRISECOUNT)/100,(AUTISM.ANGRYCOUNT+AUTISM.DISGUSTCOUNT+
                #    AUTISM.FEARCOUNT+AUTISM.SADCOUNT)/100
                #FROM AUTISM WHERE AUTISM.USERNAME = {})
		        #WHERE DATABASE.USERNAME = {} """.format (str(username), str(username)))
                cur.execute("""UPDATE DATABASE SET (AGE,ID1,ID2,ANGRYCOUNT,DISGUSTCOUNT,FEARCOUNT,HAPPYCOUNT,SADCOUNT,SURPRISECOUNT,NEUTRALCOUNT,
                TEMPERATURE,HEARTRATE,POSITIVE_EMOTIONS,NEGATIVE_EMOTIONS) = (SELECT AUTISM.AGE,AUTISM.ID4,AUTISM.ID5,AUTISM.ANGRYCOUNT,
                AUTISM.DISGUSTCOUNT,AUTISM.FEARCOUNT,AUTISM.HAPPYCOUNT,AUTISM.SADCOUNT,AUTISM.SURPRISECOUNT,AUTISM.NEUTRALCOUNT,AUTISM.TEMPERATURE,
                AUTISM.HEARTRATE,(AUTISM.HAPPYCOUNT+AUTISM.NEUTRALCOUNT+AUTISM.SURPRISECOUNT)/100,(AUTISM.ANGRYCOUNT+AUTISM.DISGUSTCOUNT+
                    AUTISM.FEARCOUNT+AUTISM.SADCOUNT)/100
                FROM AUTISM WHERE AUTISM.USERNAME = "{}")
		        WHERE DATABASE.USERNAME = "{}" """ .format(str(username), str(username)))
                con.commit()
                
############################################################
def model(videoname,username):
    
    filename = "emotion_model.h5"

    h5 = h5py.File(filename,'r')

    #futures_data = h5['futures_data']  # VSTOXX futures data
    #options_data = h5['options_data']  # VSTOXX call option data




    ###########################

    MODELPATH = 'emotion_model.h5'
    emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Sad", 5: "Surprise", 6: "Neutral"}

    model = load_model(MODELPATH)

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    #Capture Realtime Video
    #video_capture = cv2.VideoCapture(0)
    #Capture Video from file
    #videofile_path=videofile_path+file.filename
    
    #Utkarsh Path
    #videofile_path='C:\\Users\\Public\\OneDrive\\Desktop\\AUTISM\\'+videoname
    #print(videofile_path)
    #videofile_path='Database_Video/head-pose-face-detection-female-and-male.mp4'

    #Aadarsh Path
    videofile_path='C:\\Users\\aadar\\Desktop\\AUTISM\\'+videoname
    print(videofile_path)

    strext=str.split(videofile_path,'.')
    ext=strext[1]

    input_video = cv2.VideoCapture(videofile_path)

    #length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_number = 0
    Observed_Emotions=[]
    while True:
        
        # Capture frame-by-frame
    #    ret, frame = video_capture.read()
        ret, frame = input_video.read()
        frame_number += 1
        
        # Quit when the input video file ends
        if not ret:
            break
        if ext=='MOV':
            frame1 = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            frame1 = cv2.resize(frame1,(270,480))
            frame1=frame
            
        
        frame1=frame
        gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    #    im = cv2.resize(img, (Orgimg.shape[1],Orgimg.shape[0]))
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
    #        minSize=(30, 30),
    #        flags=cv2.CASCADE_SCALE_IMAGE
        
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)
            
            prediction = model.predict(cropped_img)
            emotion=emotion_dict[int(np.argmax(prediction))]
            Observed_Emotions.append(emotion)
            
            cv2.putText(frame1, emotion_dict[int(np.argmax(prediction))], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
            
    #        roi_color = frame[y:y+h, x:x+w]
    #        eyes = eye_cascade.detectMultiScale(roi_gray)
    #        for (ex,ey,ew,eh) in eyes:
    #            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        # Display the resulting frame
        cv2.imshow('Video', frame1)
        time.sleep(0.05)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # When everything is done, release the capture
    print(username)
    counting(Observed_Emotions,username)
    input_video.release()
    cv2.destroyAllWindows()
    h5.close()

