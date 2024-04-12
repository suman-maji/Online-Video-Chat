import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
from vidstream import *
import socket
import cv2;
####getting local Ip address
local_ip_address = socket.gethostbyname(socket.gethostname())
###configure reciver
Vidrecv = StreamingServer(local_ip_address, 5050)
Audrecv = AudioReceiver(local_ip_address, 5555)
####check for IP address
def chkIp(ip):
    try:
        lst1 = [int(i) for i in ip.split('.')];
    except:
        ec.config(text="[IP ERROR] What You entered ,\n is not a IP address!") 
        return False;
    else:
        if(len(lst1) == 4):
            return True;
        else:
            ec.config(text="[IPV4 ERROR] what you have entered,\n Is not a IPV4 address!")
            return False; ### starting Both server()
#####Starting Video
def startVideo(target_ip):
    camClint = CameraClient(target_ip , 7070)
    t1 = threading.Thread(target=camClint.start_stream);
    t1.start();
### Starting Audio
def startAudio(target_ip):
    audClint = AudioSender(target_ip , 7777)
    t2 = threading.Thread(target=audClint.start_stream);
    t2.start();
def Vidbtn():
    print("btn1")
    target_ip = targetIp.get(1.0 , "end-1c")
    if(chkIp(target_ip)):
        try:
            startVideo(target_ip);
        except Exception as e:
            ec.config(text="[ERROR!] Some error had occured\n check your connection and Input!")
            print(e);
        else:
            btn1.config(state=DISABLED)
def Audbtn():
    target_ip = targetIp.get(1.0 , "end-1c");
    if(chkIp(target_ip)):
        try:
            startAudio(target_ip);
        except Exception as e:
            ec.config(text="[ERROR!] Some error had occured\n check your connection and Input!")
            print(e);
        else:
            btn2.config(state=DISABLED)
##### main gui
disp = ttk.Window(themename="superhero")
disp.title("VidChat");
disp.geometry("600x400")
##Front command
f0= ttk.Frame();
f0.pack(pady=(20,3));
ec = ttk.Label( f0 , text="Welcome to our video calling App \n we are alwys ready to serve You ~" , bootstyle="inverse-primary" , padding=(32 , 12) , font=("Helvetica",13) )
ec.pack();
##setting level
ipAddress = ttk.Label( text=f"Your ip address is : {local_ip_address}" , bootstyle="inverse-sucess" , padding=(12 , 12) , font=("Helvetica",11) )
ipAddress.pack(pady=(20,10) )
# targetIp = ttk.Entry(bootstyle="Primary") ;
f1 = tk.Frame();
f1.pack(pady=(20,15));
ss = ttk.Label( f1 ,text="Enter Your Friend's ip address : " , bootstyle="secondery" , padding=( 8 , 8) , font=12 )
ss.pack( side= LEFT);
targetIp = tk.Text(f1 , height=1.1, width=(30) ) ;
# targetIp.insert(2,"ggS")
targetIp.pack(pady=(3,4) , padx=10 , side=LEFT);
f2 = tk.Frame();
f2.pack(pady=(10,0))
btn1 = ttk.Button( f2 ,text="Start Video" ,bootstyle="info-outline" , command=Vidbtn , padding=(40,10))
btn1.pack(side=LEFT)
btn2 = ttk.Button( f2 ,text="Start Audio" ,bootstyle="info-outline" , command=Audbtn , padding=(40,10))
btn2.pack(side=LEFT , padx=15)
##starting the receiving server 
vidThread = threading.Thread(target=Vidrecv.start_server);
audThread = threading.Thread(target=Audrecv.start_server);
vidThread.start();
audThread.start();
#### gui mainloop
disp.mainloop();##stoping reciving server
Vidrecv.stop_server();
Audrecv.stop_server();
cv2.destroyAllWindows();
exit();