import socket
import subprocess
import time
import json
import os
os.environ["DISPLAY"] = ":0"

UDP_IPS = ["255.255.255.255"]  # Replace with your Pis' IPs
UDP_PORT = 5005
VIDEO_PATH = "/home/pi/GeoGuessr/video.mp4"

def get_video_duration(path):
    """Returns duration in seconds as a float."""
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    info = json.loads(result.stdout)
    return float(info['format']['duration'])

def send_trigger():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Allow sending to the broadcast address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    for ip in UDP_IPS:
        sock.sendto(b"PLAY", (ip, UDP_PORT))
    print("Sent PLAY trigger to all Pis!")

def play_local_vlc():
    # Focus VLC window
    subprocess.run('xdotool search --name "VLC media player" windowactivate --sync', shell=True)
    # Seek to start (Home key)
    subprocess.run('xdotool key Home', shell=True)
    # Press space (play, just in case)
    subprocess.run('xdotool key space', shell=True)


if __name__ == "__main__":
    # Wait for all listeners and VLC windows to be ready
    time.sleep(10)

    # Get the duration of the video in seconds
    video_duration = get_video_duration(VIDEO_PATH)
    print(f"Detected video duration: {video_duration:.2f} seconds")

    while True:
        print("Starting playback round!")
        send_trigger()
        play_local_vlc()
        time.sleep(video_duration)
