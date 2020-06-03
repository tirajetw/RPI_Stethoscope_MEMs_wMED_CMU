# RPI_Stethoscope_MEMs_wMED_CMU
This project uses for make device to record sound of lung from Covid-19 Disease Patients

Prepare before running this project.
- Install Raspbian on an SD Card
- Installer Script
```
cd ~
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.sh
chmod +x i2smic.sh
sudo ./i2smic.sh
```
- Adding Volume Control : You can add volume control to your mic via alsamixer and alsa config. To do so, create and edit a file .asoundrc in your home directory.
```
nano ~/.asoundrc
```
and put the following in this file:
```
#This section makes a reference to your I2S hardware, adjust the card name
# to what is shown in arecord -l after card x: before the name in []
#You may have to adjust channel count also but stick with default first
pcm.dmic_hw {
	type hw
	card sndrpii2scard
	channels 2
	format S32_LE
}

#This is the software volume control, it links to the hardware above and after
# saving the .asoundrc file you can type alsamixer, press F6 to select
# your I2S mic then F4 to set the recording volume and arrow up and down
# to adjust the volume
# After adjusting the volume - go for 50 percent at first, you can do
# something like 
# arecord -D dmic_sv -c2 -r 48000 -f S32_LE -t wav -V mono -v myfile.wav
pcm.dmic_sv {
	type softvol
	slave.pcm dmic_hw
	control {
		name "Boost Capture Volume"
		card sndrpii2scard
	}
	min_dB -3.0
	max_dB 30.0
}
```
- Then run ```alsamixer``` and press F6 and select the I2S sound card
- Press F4 to switch to Capture mode and you should be able to adjust the volume with up/down arrow keys.

ref : https://learn.adafruit.com/adafruit-i2s-mems-microphone-breakout/raspberry-pi-wiring-test


How to use
- Install Python package requirement
```
pip3 install pytz
pip3 install pysftp
pip3 install gpiozero
```
- Clone this project to raspberry-pi
```
git clone https://github.com/tirajetw/RPI_Stethoscope_MEMs_wMED_CMU.git
```
- cd RPI_Stethoscope_MEMs_wMED_CMU
- config your sftp server in file main.py
```
myHostname = ""
myUsername = ""
myPassword = ""
SFTPfilepath = "RPI_Stethoscope_MEMs_wMED_CMU/recfile/"
```
- then, run ```python3 main.py``` and push button in raspberry pi steththoscope module to record and send file to server via sftp.