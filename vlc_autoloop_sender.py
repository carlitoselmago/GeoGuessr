import socket
import subprocess
import time
import json
import os
import threading

os.environ["DISPLAY"] = ":0"

UDP_IPS = ["192.168.10.255"]  # Broadcast to all Pis
UDP_PORT = 5005
VIDEO_PATH = "/home/pi/GeoGuessr/video.mp4"

def get_local_ip():
    """Gets the local IP address of the current machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable; just for IP detection
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

LOCAL_IP = get_local_ip()

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

def play_local_vlc(i=0):
    print("Restarting VLC playback...")
    # Activate VLC window
    subprocess.run('xdotool search --name "VLC" windowactivate --sync', shell=True)
    # Seek to beginning
    subprocess.run('xdotool key Home', shell=True)
    if (i>0):
        subprocess.run('xdotool key p', shell=True)
    else:
        # Start playback
        subprocess.run('xdotool key space', shell=True)


def udp_listener():
    """Listener that triggers play_local_vlc() on UDP 'PLAY', ignoring own broadcasts."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', UDP_PORT))
    print(f"Listening for UDP triggers on port {UDP_PORT} (local IP: {LOCAL_IP})")

    while True:
        data, addr = sock.recvfrom(1024)
        sender_ip = addr[0]
        if sender_ip == LOCAL_IP or sender_ip == "127.0.0.1":
            # Ignore own broadcast
            print(f"Ignored trigger from self: {sender_ip}")
            continue
        if data == b"PLAY":
            print(f"Received PLAY trigger from {sender_ip}")
            play_local_vlc()

if __name__ == "__main__":
    # Start UDP listener thread
    threading.Thread(target=udp_listener, daemon=True).start()

    # Wait for all listeners and VLC windows to be ready
    print("Sleep for 10 seconds...")
    time.sleep(10)

    # Get the duration of the video in seconds
    video_duration = get_video_duration(VIDEO_PATH)
    print(f"Detected video duration: {video_duration:.2f} seconds")
    c=0
    while True:
        print("Starting playback round!")
        send_trigger()         # Send PLAY to all followers (and self, but ignored)
        play_local_vlc(c)       # Only the sender plays locally from code
        time.sleep(video_duration - 0.5)
        c+=1
