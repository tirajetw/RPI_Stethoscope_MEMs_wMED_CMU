import os
import time
import pytz
from datetime import datetime, timedelta
import pysftp
# from gpiozero import Button

myHostname = "202.28.24.148"
myUsername = "jet"
myPassword = "s4324$"
tz = pytz.timezone('Asia/Bangkok')
button = Button(17)

while True:
    if button.is_pressed:
        print("Pressed : record 30 sec.")
        now = datetime.now(tz)
        filename = now.strftime("%Y%m%d%H%M%S")

        os.system('arecord -D dmic_sv -c2 -r 48000 -f S32_LE -t wav -V mono -v {}.wav -d 30'.format(filename))

        #  sftp file to server
        with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
            print ("Connection succesfully stablished ... ")
            localFilePath = '{}.wav'.format(filename)
            remoteFilePath = '{}.wav'.format(filename)
            sftp.put(localFilePath, remoteFilePath)
    
    else:
        print("Released")
    time.sleep(0.1)


