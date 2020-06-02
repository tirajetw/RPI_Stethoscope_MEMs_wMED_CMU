import os
import time
import pytz
from datetime import datetime, timedelta
import pysftp
from gpiozero import Button
from scipy.io import wavfile
import noisereduce as nr
import soundfile as sf
from noisereduce.generate_noise import band_limited_noise
import matplotlib.pyplot as plt
import urllib.request
import numpy as np
import io
# %matplotlib inline

myHostname = "202.28.24.148"
myUsername = "jet"
myPassword = "s4324$"
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
            localFilePath1 = 'recfile/{}_original.wav'.format(filename)
            remoteFilePath1 = 'RPI_Stethoscope_MEMs_wMED_CMU/recfile/{}_original.wav'.format(filename)
            localFilePath2 = 'recfile/{}_filtered.wav'.format(filename)
            remoteFilePath2 = 'RPI_Stethoscope_MEMs_wMED_CMU/recfile/{}_filtered.wav'.format(filename)
            # Filter segment
            data, rate = sf.read(localFilePath)
            noise_data, noise_rate = sf.read("recfile/noise_data.wav")
            noise_reduced = nr.reduce_noise(audio_clip=data, noise_clip=noise_data, prop_decrease=1.0, verbose=True) 
            wavfile.write('recfile/{}_filtered.wav'.format(filename), rate, noise_reduced)
            # SFTP segment
            sftp.put(localFilePath1, remoteFilePath1)
            sftp.put(localFilePath2, remoteFilePath2)
    
    else:
        print("Released")
    time.sleep(0.1)


