import socket
import subprocess

UDP_IP = ""
UDP_PORT = 5005

print("Waiting for PLAY trigger...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Add this line
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    if data == b"PLAY":
        print(f"Received PLAY trigger from {addr[0]}. Playing video...")
        #subprocess.run('xdotool search --name VLC windowactivate --sync key Home', shell=True)
        # Activate VLC window
        subprocess.run('xdotool search --name "VLC" windowactivate --sync', shell=True)
        subprocess.run('xdotool key p', shell=True)
        #subprocess.run('xdotool key space', shell=True)
