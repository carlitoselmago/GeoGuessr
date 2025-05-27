#!/bin/bash
export DISPLAY=:0

# Launch VLC
vlc --aout=alsa --no-video-title-show --qt-minimal-view --no-qt-fs-controller --start-paused /home/pi/GeoGuessr/video.mp4 &

# Wait for VLC window to appear (max 10s)
for i in {1..20}; do
    sleep 0.5
    # Try to find the window
    WID=$(xdotool search --name "VLC media player" | head -1)
    if [ ! -z "$WID" ]; then
        break
    fi
done

# If window is found, set properties
if [ ! -z "$WID" ]; then
    # Remove window borders (undecorated)
    wmctrl -ir "$WID" -b add,undecorated
    # Move and resize: 1440x720 at position 0,0 (adjust as needed)
    xdotool windowmove "$WID" 0 0
    xdotool windowsize "$WID" 1440 720
else
    echo "VLC window not found"
fi
