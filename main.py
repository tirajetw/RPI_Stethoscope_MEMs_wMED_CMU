import os
import time
from datetime import datetime, timedelta
import pytz
import pysftp
from gpiozero import Button

myHostname = ""
myUsername = ""
myPassword = ""
SFTPfilepath = "RPI_Stethoscope_MEMs_wMED_CMU/recfile/"
tz = pytz.timezone('Asia/Bangkok')
button = Button(17)
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None 

while True:
    if button.is_pressed:
        print("Pressed : record 30 sec.")
        now = datetime.now(tz)
        filename = now.strftime("%Y%m%d%H%M%S")

        os.system('arecord -D dmic_sv -c2 -r 48000 -f S32_LE -t wav -V mono -v {}.wav -d 30'.format(filename))

        #  sftp file to server
        with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
            print ("Connection succesfully stablished ... ")
            localFilePath = '{}.wav'.format(filename)
            remoteFilePath = SFTPfilepath + '{}.wav'.format(filename)
            sftp.put(localFilePath, remoteFilePath)
    
    else:
        print("Released")
    time.sleep(0.1)


