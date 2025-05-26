# GeoGuessr
Double screen, double player via direct cable

## Requirements
ffmpeg

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

export DISPLAY=:0

# Wait for X to be ready
sleep 5

# Launch VLC and prep window (paused, borderless)
bash /home/pi/GeoGuessr/launch_vlc.sh

# Wait for VLC to open and settle
sleep 3

# Start the Python listener (in background)
python3 /home/pi/GeoGuessr/vlc_listener.py &

# Longer wait so followers are ready and listening (adjust as needed)
sleep 10

# Send the PLAY trigger (in background, so rc.local can finish)
python3 /home/pi/GeoGuessr/play_trigger.py &

exit 0

```

### Follower
- launch_vlc.sh 
- vlc_listener.py

Demo rc.local file
```
#!/bin/bash
# rc.local for follower

# Make sure DISPLAY is set for X apps (change :0 if needed)
export DISPLAY=:0

# Wait for X to be ready
sleep 5

# Launch VLC and prep window (paused, borderless)
bash /home/pi/GeoGuessr/launch_vlc.sh

# Wait for VLC to open and settle
sleep 3

# Start the Python listener (in background)
python3 /home/pi/GeoGuessr/vlc_listener.py &

exit 0
```