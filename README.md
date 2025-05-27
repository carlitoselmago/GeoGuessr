# GeoGuessr
Double screen, double player via direct cable, using X GUI

## Requirements
```
sudo apt-get install wmctrl xdotool ffmpeg
```
Also vlc if not installed

## Installation
- if new versions of raspios:
```
sudo nano /etc/rc.local
```
And copy the right file for each
```
sudo chmod +x /etc/rc.local
sudo systemctl enable rc-local.service
sudo reboot
```
Check /boot/config.txt for custom screen configuration of 720x720 dual screen, change accordingly

If using direct ethernet cable, you should configure manually an ip range for both raspberrys, specially if also using wifi for debugging
You want the signals sent by ethernet, not wifi

To setup static ips from terminal (this will be permanent after reboot)
Sender
```
sudo nmcli con add type ethernet ifname eth0 con-name eth0-static ip4 192.168.10.1/24
sudo nmcli con up eth0-static
```
Follower
```
sudo nmcli con add type ethernet ifname eth0 con-name eth0-static ip4 192.168.10.2/24
sudo nmcli con up eth0-static
```

## Structure

Run launch_vlc.sh on all raspberrys, on follower run vlc_listener.py
Then when ready (with a bigger pause than follower) run vlc_autoloop_sender.py on Sender which will take care of sending the play messages to followers

### Sender
- launch_vlc.sh 
- vlc_autoloop_sender.py

Demo rc.local file
```
#!/bin/bash
# rc.local for sender

# Wait for X to be ready (increase if your X takes longer to start)
sleep 5

# Launch VLC as user 'pi', with X11 authorization
sudo -u pi DISPLAY=:0 XAUTHORITY=/home/pi/.Xauthority bash /home/pi/GeoGuessr/launch_vlc.sh

# Wait for VLC to open and settle
sleep 3

# Start the Python listener as user 'pi' (if it needs X), or as root if it does not need X
#sudo -u pi DISPLAY=:0 XAUTHORITY=/home/pi/.Xauthority python3 /home/pi/GeoGuessr/vlc_listener.py &

# Longer wait so followers are ready and listening (adjust as needed)
sleep 10

# Send the PLAY trigger (usually doesn't need X, but if it does, same as above)
sudo -u pi DISPLAY=:0 XAUTHORITY=/home/pi/.Xauthority python3 /home/pi/GeoGuessr/vlc_autoloop_sender.py &

exit 0


```

### Follower
- launch_vlc.sh 
- vlc_listener.py

Demo rc.local file
```
#!/bin/bash
# rc.local for follower

# Wait for X to be ready
sleep 5

# Launch VLC as user 'pi', with X11 authorization
sudo -u pi DISPLAY=:0 XAUTHORITY=/home/pi/.Xauthority bash /home/pi/GeoGuessr/launch_vlc.sh

# Wait for VLC to open and settle
sleep 3

# Start the Python listener (in background)
sudo -u pi DISPLAY=:0 XAUTHORITY=/home/pi/.Xauthority python3 /home/pi/GeoGuessr/vlc_listener.py &

exit 0
```