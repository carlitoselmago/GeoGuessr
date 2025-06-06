import socket
import subprocess
import time

UDP_IP = ""
UDP_PORT = 5005

print("Waiting for PLAY trigger...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Add this line
sock.bind((UDP_IP, UDP_PORT))

c=0

while True:
    data, addr = sock.recvfrom(1024)
    if data == b"PLAY":
        print(f"Received PLAY trigger from {addr[0]}. Playing video...")
        #subprocess.run('xdotool search --name VLC windowactivate --sync key Home', shell=True)
        # Activate VLC window
        subprocess.run('xdotool search --name "VLC" windowactivate --sync', shell=True)
        if c>0:
            print("Seek to start")
            subprocess.run('xdotool key p', shell=True)
            time.sleep(1)
        
        subprocess.run('xdotool key space', shell=True)
        c+=1
