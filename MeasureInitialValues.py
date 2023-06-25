from datetime import datetime
from config.database_config import *

import paho.mqtt.client as mqtt
# import sys
# pip install pymongo
# import cv2
# import pymongo
# from ffpyplayer.player import MediaPlayer
import warnings
# import numpy as np
# from sys import exit
import time
from statistics import mean

BROKER = 'broker.emqx.io'
PORT = 1883
TOPIC = "/sensors/initialValues"
CLIENT_ID = f'python-mqtt-3'
normal_values = []
stress_values = []
USER = 0


# username = 'emqx'
# password = 'public'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload) + 'received at: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if str(msg.payload).startswith("normal:"):
        value = int(str(msg.payload).split(":")[1].split("'")[0])
        if value > 0:
            normal_values.append(value)
    else:
        value = int(str(msg.payload).split(":")[1].split("'")[0])
        if value > 0:
            stress_values.append(value)


# def PlayVideo(video_path):
#    video=cv2.VideoCapture(video_path)
#    player = MediaPlayer(video_path)
#    while True:
#        grabbed, frame=video.read()
#        audio_frame, val = player.get_frame()
#        if not grabbed:
#            print("End of video")
#            break
#        if cv2.waitKey(28) & 0xFF == ord("q"):
#            break
#        cv2.imshow("Video", frame)
#        if val != 'eof' and audio_frame is not None:
#            #audio
#            img, t = audio_frame
#    video.release()
#    cv2.destroyWindow('Video')
#    cv2.waitKey(1)
#    

def run():
    employees = ["meiaagent@lightwitch.org", "meiaagent1@lightwitch.org", "meiaagent2@lightwitch.org",
                 "meiaagent3@lightwitch.org"
                 "meiaagent4@lightwitch.org", "meiaagent5@lightwitch.org", "meiaagent6@lightwitch.org"]
    warnings.filterwarnings("ignore")
    print("Choose the employee:")
    print("1. meiaagent@lightwitch.org")
    print("2. meiaagent1@lightwitch.org")
    print("3. meiaagent2@lightwitch.org")
    print("4. meiaagent3@lightwitch.org")
    print("5. meiaagent4@lightwitch.org")
    print("6. meiaagent5@lightwitch.org")
    print("7. meiaagent6@lightwitch.org")
    employee = input("Enter the number of the employee: ")
    print(employee)
    print("Now watch the video")
    # PlayVideo('Initial Measures.mp4')

    client = mqtt.Client(CLIENT_ID)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    # emp = "user:"+str(employees[int(employee)-1])
    # client.subscribe(TOPIC, emp)
    t_end = time.time() + 80
    client.subscribe(TOPIC)
    client.loop_start()
    while time.time() < t_end:
        client.on_message = on_message
    client.loop_stop()
    normal_value = 0
    stress_value = 0

    if len(normal_values) > 0:
        normal_value = mean(normal_values)
    if len(stress_values) > 0:
        stress_value = mean(stress_values)

    USER = str(employees[int(employee) - 1])
    print(USER)
    print(normal_value)
    print(stress_value)

    # normal_value = 250
    # stress_value = 350

    myquery = {"username": USER}
    new_values = {"$set": {"avg_force": normal_value, "stress_level": stress_value}}

    USERS.update_one(myquery, new_values)


if __name__ == "__main__":
    run()
