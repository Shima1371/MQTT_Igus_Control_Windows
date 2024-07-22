# -*- coding: utf-8 -*-
from threading import Thread
import threading
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
# from dobot_api import *
import json
from paho.mqtt import client as mqtt
import re
import socket
import sys
from pymodbus.client import ModbusSerialClient as ModbusClient

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


class MQTTWin(object):
    def __init__(self,root):
        self.lastErr = time.time()*1000 # epoch millisecond
        self.defPose =  ['284', '129', '393', '-174', '42', '-175']
        self.curPose = ['0','0','0','0','0','0']
        self.jogvalues = ['0.0','0.0','0.0','0.0','0.0','0.0']
        self.lx = 0
        self.ly= 0
        self.lz  =0
        self.global_state = {}
        self.global_state["connect"] = False

        self.root = root
        self.root.title("MQTT-igus Controller")
        self.root.geometry("600x800")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.mqbutton = Button(self.root, text="Conn Igus", padx=5,
                             command=self.my_connect)
        self.mqbutton.grid(row=0,column=0,padx=2,pady=10)
        
        #2回押すとアクセス拒否
        self.mv2button = Button(self.root, text="Connect SCB-PB", padx=5,
                             command=self.connect_scb_pb)
        self.mv2button.grid(row=0,column=1,padx=2,pady=10)

        self.mqbutton = Button(self.root, text="Connect MQTT", padx=5,
                             command=self.connect_mqtt)
        self.mqbutton.grid(row=0,column=2,padx=2,pady=10)
    

        self.enable = Button(self.root, text="SetActive", padx=5,
                             command=self.setActive)
        self.enable.grid(row=0,column=3,padx=2,pady=10)

        self.mvbutton = Button(self.root, text="Test1", padx=5,
                             command=self.testMove)
        self.mvbutton.grid(row=0,column=4,padx=2,pady=10)

        self.mv3button = Button(self.root, text="Grasp", padx=5,
                             command=self.grasp)
        self.mv3button.grid(row=0,column=5,padx=2,pady=10)
        self.mv4button = Button(self.root, text="Release", padx=5,
                             command=self.release)
        self.mv4button.grid(row=0,column=6,padx=2,pady=10)
        
        self.mvbutton = Button(self.root, text="Test2", padx=5,
                             command=self.testMove2)
        self.mvbutton.grid(row=0,column=7,padx=2,pady=10)
        
        self.mvbutton = Button(self.root, text="Test3", padx=5,
                             command=self.testMove3)
        self.mvbutton.grid(row=0,column=8,padx=2,pady=10)

#         self.mv5button = Button(self.root, text="ClearErr", padx=5,
#                              command=self.clear_error)
#         self.mv5button.grid(row=0,column=7,padx=2,pady=10)

        self.info_frame = LabelFrame(self.root, text="info", labelanchor="nw",
                                     bg="#FFFFFF", width=550, height=150)
        self.info_frame.grid(row=1, column=0, padx=5,pady=5,columnspan=8)

#         self.label_robot_mode = Label(self.info_frame, text="")
#         self.label_robot_mode.place(rely=0.1, x=10)

#         self.label_feed_speed = Label(self.info_frame,text="")
#         self.label_feed_speed.place(rely=0.1, x=245)

# #        self.set_label(self.frame_feed, text="%", rely=0.05, x=175)



        self.xplus = Button(self.root, text="DefaultPose", padx=5,
                             command=self.defaultPose)
        self.xplus.grid(row=2,column=0,padx=2,pady=10)

#         self.yplus = Button(self.root, text="SetDefPose", padx=5,
#                              command=self.setDefPose)
#         self.yplus.grid(row=2,column=1,padx=2,pady=10)

        self.enb = Button(self.root, text="EnableRobot", padx=5,
                             command=self.enableRobot)
        self.enb.grid(row=2,column=3,padx=2,pady=10)

        self.enb = Button(self.root, text="DisableRobot", padx=5,
                             command=self.disableRobot)
        self.enb.grid(row=2,column=4,padx=2,pady=10)

        self.text_log = tk.scrolledtext.ScrolledText(self.root,width=70,height=60)
        self.text_log.grid(row=3,column =0, padx=10, pady=10,columnspan=7)

        self.text_log.insert(tk.END,"Start!!")
        
    def log_txt(self,str):
        self.text_log.insert(tk.END,str)
        
    def on_close(self):
        """ウィンドウが閉じられるときに呼ばれる関数"""
        self.global_state["connect"] = False
        # 他のクリーンアップ作業が必要な場合はここに追加
        self.root.destroy()  # ウィンドウを閉じる
        
    def defaultPose(self):
        pose = self.defPose
        message = "CRISTART 1234 CMD Move Cart "+pose[0]+" "+pose[1]+" "+pose[2]+" "+pose[3]+" "+pose[4]+" "+pose[5]+" 0 0 0 100 #base CRIEND"
        encoded=message.encode('utf-8')
        array=bytearray(encoded)
        sock.sendall(array)
        self.log_txt("defaultPose"+"\n")
        
    def setActive(self):
        message = "CRISTART 1234 CMD GetActive CRIEND"
        message = "CRISTART 1234 CMD SetActive true CRIEND"
        encoded=message.encode('utf-8')
        array=bytearray(encoded)
        # Send the main message
        self.log_txt("setActive"+"\n")
        sock.sendall(array)      

        
    def enableRobot(self):
        message = "CRISTART 1234 CMD Enable CRIEND"
        encoded=message.encode('utf-8')
        array=bytearray(encoded)
        # Send the main message
        self.log_txt("Enable Robot"+"\n")
        sock.sendall(array)
        
    def disableRobot(self):
        message = "CRISTART 1234 CMD Disable CRIEND"
        encoded=message.encode('utf-8')
        array=bytearray(encoded)
        # Send the main message
        self.log_txt("Disable Robot"+"\n")
        sock.sendall(array)
    
    def resetRobot(self):
        self.lx = 0
        self.ly = 0
        self.lz = 0
        self.lxd = 0
        self.lyd = 0
        self.lzd = 0
        self.text_log.delete('1.0', 'end-1c')
    
    def my_connect(self):
        # Enter the IP address of the robot ('192.168.3.11', 3920) here if you're not using a CPRog/iRC simulation ('127.0.0.1', 3921)
        # MEMO: my PC ('172.19.16.1', 3921)
        server_address = ('192.168.3.11', 3920)
        self.log_txt("Connecting..."+"\n")
        sock.connect(server_address)
        self.log_txt("Connected"+"\n")
        
        self.global_state["connect"] = not self.global_state["connect"]
        
        self.set_keep_alive()
        self.set_receive_message()
        message = "CRISTART 1234 CMD MotionTypeCartBase CRIEND"
        encoded=message.encode('utf-8')
        array=bytearray(encoded)
        # Send the main message
        self.log_txt("Set the motion type Cartbase"+"\n")
        sock.sendall(array)
        
    def set_keep_alive(self):
        if self.global_state["connect"]:
            thread = threading.Thread(target=self.keep_alive)
            thread.start()

    def keep_alive(self):
        # I'm sending 10 more ALIVEJOG messages to keep the connection alive.
        # If I drop the connection too early our message may not get through.
        # A production program should send this once or twice a second from a parallel thread.
        while True:
            if not self.global_state["connect"]:
                break
            
            jogvalues = self.jogvalues
            messageAliveJog = "CRISTART 1234 ALIVEJOG "+jogvalues[0]+" "+jogvalues[1]+" "+jogvalues[2]+" "+jogvalues[3]+" "+jogvalues[4]+" "+jogvalues[5]+" 0.0 0.0 0.0 CRIEND"
            encodedAliveJog=messageAliveJog.encode('utf-8')
            arrayAliveJog=bytearray(encodedAliveJog)
            print("message:", messageAliveJog)
            # self.log_txt("Keeping connection alive"+"\n")
            # print("Sending ALIVEJOG")
            sock.sendall(arrayAliveJog)
            # print(arrayAliveJog)
            time.sleep(0.02)
            
    def set_receive_message(self):
        if self.global_state["connect"]:
            thread = threading.Thread(target=self.receive_message)
            thread.start()
            
            
    def receive_message(self):
        while True:
            if not self.global_state["connect"]:
                break
            data = sock.recv(4096)
            self.lastMessage = data.decode()
    
# ブローカーに接続できたときの処理
    def on_connect(self,client, userdata, flag, rc):
        print("Connected with result code " + str(rc))  # 接続できた旨表示
        self.client.subscribe("webxr/pose2") #　connected -> subscribe
        self.log_txt("Connected MQTT"+"\n")

# ブローカーが切断したときの処理
    def on_disconnect(self,client, userdata, rc):
        if  rc != 0:
            print("Unexpected disconnection.")

    def on_message(self,client, userdata, msg):
        js = json.loads(msg.payload)
        # print("Message!",js)

        if 'pos' in js:
            x = js['pos']['x']
            y = js['pos']['y']
            z = js['pos']['z']
            xd = js['ori']['x']
            yd = js['ori']['y']
            zd = js['ori']['z']
            # print(x, y, z, xd, yd, zd)
        else:
            print("JSON",js)
            return
        
        if self.lx ==0 and self.ly == 0 and self.lz ==0:
            self.lx = x
            self.ly = y
            self.lz = z
            self.lxd = xd
            self.lyd = yd
            self.lzd = zd
        if True:
            dx = x-self.lx
            dy = y-self.ly
            dz = z-self.lz
            dxd = xd-self.lxd
            dyd = yd-self.lyd
            dzd = zd-self.lzd
            # print(dxd,dyd,dzd)
            sc = 2000
            dx *= sc
            dy *= sc
            dz *= sc
            # print(dx,dy,dz)


            if 'pad' in js:
                pd = js['pad']
                if pd['bA']:
                    print("reset")
                    self.resetRobot()


                if abs(dx)>= 5 or abs(dy)>= 5 or abs(dz)>= 5 or abs(dxd)>=0.1 or abs(dyd)>=0.1 or abs(dzd)>=0.1:
                    if pd['b0']!=1:
                        self.jogvalues = [str(self.clamp_value(-dz)),str(self.clamp_value(-dx)),str(self.clamp_value(dy)),str(self.clamp_value(dzd*1800)),str(self.clamp_value(-dxd*1800)),str(self.clamp_value(dyd*1800))]
                    else:
                        self.jogvalues =  ['0.0','0.0','0.0','0.0','0.0','0.0']
                else:
                    self.jogvalues =  ['0.0','0.0','0.0','0.0','0.0','0.0']
                
                self.lx = x
                self.ly = y
                self.lz = z
                self.lxd = xd
                self.lyd = yd
                self.lzd = zd
        
                if pd['bm']!=1:
                    self.release()
                else:
                    self.grasp()
                    


    def clamp_value(self, x):
        return max(-100, min(100, x))
            
    def connect_mqtt(self):
        self.client = mqtt.Client()  
# MQTTの接続設定
        self.client.on_connect = self.on_connect         # 接続時のコールバック関数を登録
        self.client.on_disconnect = self.on_disconnect   # 切断時のコールバックを登録
        self.client.on_message = self.on_message         # メッセージ到着時のコールバック
        self.client.connect("192.168.207.22", 1883, 60)
#  client.loop_start()   # 通信処理開始
        self.client.loop_start()   # 通信処理開始
        
    def connect_scb_pb(self):
        # Modbus RTUクライアントの設定
        self.modbus_client = ModbusClient(method='rtu', port='COM3',stopbits=1, bytesize=8, parity='N', baudrate=38400, timeout=3) #baudrate=38400
        # クライアントの接続
        connection = self.modbus_client.connect()
        if connection:
            self.log_txt("SCB-PB is Connected"+"\n")
        return self.modbus_client
    
    def getPose(self):
        now= time.time()*1000
        if now - self.lastErr < 500: # 最後のエラーから　500msec
            return None
        if self.lastMessage:
            # POSCARTROBOTに続く6個の数字を抽出
            self.curPose = self.extract_pos_cart_robot(self.lastMessage)
            # print("POSCARTROBOT positions:", pos_cart_robot)
            return self.curPose
    
    def extract_pos_cart_robot(self, message):
        # 正規表現を使用してPOSCARTROBOTの位置情報を探す
        match = re.search(r'POSCARTROBOT\s+([-+]?\d+\.?\d*)\s+([-+]?\d+\.?\d*)\s+([-+]?\d+\.?\d*)\s+([-+]?\d+\.?\d*)\s+([-+]?\d+\.?\d*)\d*\s+([-+]?\d+\.?\d*)', message)
        if match:
            return [float(num) for num in match.groups()]
        return None
        
    # def relativeMove(self,y,z,x,yd,zd,xd):
    #     pose = self.getPose()
        
    #     if pose:
    #         pose[0]=str(100.0) if float(pose[0])-x > 0 else str(-100.0)
    #         pose[1]=str(100.0) if float(pose[1])-y > 0 else str(-100.0)
    #         pose[2]=str(100.0) if float(pose[2])+z > 0 else str(-100.0)
    #         pose[3]=str(100.0) if float(pose[3])-xd > 0 else str(-100.0)
    #         pose[4]=str(100.0) if float(pose[4])+yd > 0 else str(-100.0)
    #         pose[5]=str(100.0) if float(pose[5])+zd > 0 else str(-100.0)
    #         message = "CRISTART 1234 ALIVEJOG "+pose[0]+" "+pose[1]+" "+pose[2]+" 0.0 0.0 0.0 0.0 0.0 0.0 CRIEND" #角度反映
    #         encoded=message.encode('utf-8')
    #         array=bytearray(encoded)
    #         sock.sendall(array)
    #         print("input:",y,z,x,xd,yd,zd)
    #         print("message:", message)
    #         time.sleep(0.1)
        
        #getPose()をしない分速いかもしれないが、コントローラの角度は反映されない
        # if True:
        #     x=str(-x)
        #     y=str(-y)
        #     z=str(z)
        #     xd=str(xd)
        #     yd=str(yd)
        #     zd=str(zd)
        #     message = "CRISTART 1234 CMD Move RelativeBase "+x+" "+y+" "+z+" "+xd+" "+yd+" "+zd+" 0 0 0 200 #base CRIEND" #コマンドの仕様上RelativeBaseではxd, yd, zdが無視される
        #     encoded=message.encode('utf-8')
        #     array=bytearray(encoded)
        #     sock.sendall(array)
        #     print("input:",y,z,x,xd,yd,zd)
        #     print("message:", message)
#            self.log_txt("Relavtive x:"+str(int(xd*100))+"y: "+str(int(yd*100))+" z:"+str(int(zd*100))+"\n")
        
    def testMove(self):
        pose = ["0","0","0","0","0","0"]
        pose[0]=str(225)
        pose[1]=str(0)
        pose[2]=str(320)
        pose[3]=str(170)
        pose[4]=str(0)
        pose[5]=str(-175)
        message = "CRISTART 1234 CMD Move Cart "+pose[0]+" "+pose[1]+" "+pose[2]+" "+pose[3]+" "+pose[4]+" "+pose[5]+" 0 0 0 200 #base CRIEND"
        encoded=message.encode('utf-8')
        array=bytearray(encoded)
        # Send the main message
        self.log_txt("Test1"+"\n")
        sock.sendall(array)
        
    def testMove2(self):
        self.jogvalues =  ['0.0','0.0','0.0','50.0','0.0','0.0']
        print(self.jogvalues)
        
    def testMove3(self):
        self.jogvalues =  ['-50.0','0.0','0.0','0.0','0.0','0.0']
        print(self.jogvalues)

        
    def grasp(self):
        response = self.modbus_client.write_register(address=1, value=1, slave=1)
    
    def release(self):
        response = self.modbus_client.write_register(address=1, value=3, slave=1)

        
root = tk.Tk()

mqwin = MQTTWin(root)
mqwin.root.lift()
root.mainloop()
