import socket
import subprocess

UDP_IP = ""
UDP_PORT = 5005

print("Waiting for PLAY trigger...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    if data == b"PLAY":
        print("Received PLAY trigger. Sending space to VLC...")
        subprocess.run('xdotool search --name "VLC media player" windowactivate --sync key space', shell=True)
