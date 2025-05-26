#!/bin/bash
export DISPLAY=:0
vlc --no-video-title-show --qt-minimal-view --no-qt-fs-controller --start-paused /home/pi/GeoGuessr/video.mp4 &
sleep 2
wmctrl -r "VLC media player" -b add,undecorated
xdotool search --name "VLC media player" windowmove %@ 0 0