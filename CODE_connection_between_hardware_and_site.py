import serial #Serial package for read/write from arduino

port = '/dev/ttyACM0'  #'COM28' #Change this to your port which is connected to arduino use '/dev/ttyS0' template for linux

arduino = serial.Serial(port,115200,timeout=10) #Define the Serial port which the arduino is connected to

P = list(range(6)) #P1,P2,P3,P4,PQ(later will be P5),PS (later will be P6)
Pstatus = '0000' #Victor Status 1,2 or 3
 
#Creat Auto or Manual file 
f= open("/var/www/html/Login_v8-site1/autoOrManual.txt",'w+')
serverStatus = '1' #1 for auto 2 for manual
f.write(serverStatus)
f.close()

#Save Auto or Manual status
lastServerStatus = serverStatus

Pstatus_Manual_Last=1111
flag_msg_x=0
while(True):
    
    msg = arduino.readline() #Read What the arduino has sent
    if arduino.inWaiting()==0:
        #print("ERROR")
        pass
        
    msg = str(msg.decode('utf-8',errors='ignore'))
    #msg =unicode(msg,)
    #msg = str(msg)
    print(msg)
    if(len(msg)==0):
        continue
    f= open("/var/www/html/Login_v8-site1/autoOrManual.txt",'r')
    serverStatus = f.read()
    f.close()
    if lastServerStatus == serverStatus: #User didn't change auto/manual using the website
        while(msg):
            if msg[-1].isdigit():
                break
            else:
                msg = msg[:-1]
        if(len(msg)==0):
            continue
        else:
            serverStatus = msg[-1]
            lastServerStatus = serverStatus
            f= open("/var/www/html/Login_v8-site1/autoOrManual.txt","w+")
            f.write(serverStatus)
            f.close()
        if(len(msg)==0):
            continue
    elif lastServerStatus != serverStatus:  #User did change the auto/manual using the website
         lastServerStatus = serverStatus
    index = -1
    for i in range(6): #This for loop will extract P1 to P6 from the message and save each one in a file
        index = msg.find('P',index+1)
        P[i] = msg[index+3:msg.find('P',index+1)]
        fileName = "/var/www/html/Login_v8-site1/"+"p"+str(i+1)+".txt"
        f= open(fileName,"w+")
        f.write(P[i])
        f.close()
    index = msg.find('@')
    #This  will extract the station status victor and save it in a file
    Pstatus = msg[index+1:index+5]
    if Pstatus_Manual_Last!=Pstatus:
        flag_msg_x=1
        Pstatus_Manual_Last=Pstatus
    elif Pstatus_Manual_Last==Pstatus:
        flag_msg_x=0
    if flag_msg_x==1:
        fileName = "/var/www/html/Login_v8-site1/Station Status.txt"
        f= open(fileName,"w+")
        f.write(Pstatus)
        f.close()
    if serverStatus=='1': #AUTO
        index = msg.find('@')
        #This  will extract the station status victor and save it in a file
        Pstatus = msg[index+1:index+5]
        fileName = "/var/www/html/Login_v8-site1/Station Status.txt"
        f= open(fileName,"w+")
        f.write(Pstatus)
        f.close()
        arduino.write("done".encode('utf-8')) #Just to let the arduino know that we are done readingjkio
    elif serverStatus == '2': #Manual
        #This will read the status victor file and send it to Arduino
        f= open("/var/www/html/Login_v8-site1/Station Status.txt",'r')
        contents = f.read()
        f.close()
        arduino.write(contents.encode('utf-8'))
        #arduino.write("manu".encode('utf-8'))
    #arduino.write("q".encode('utf-8'))
