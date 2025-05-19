import socket
import paramiko
import threading
from datetime import datetime

LOG_FILE = "logs/ssh_logins.log"
BIND_PORT = 2222  # Gunakan 22 kalau berani 😈 (butuh root)

class SSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.event = threading.Event()
        self.client_ip = client_ip

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        with open(LOG_FILE, "a") as log:
            log.write("="*60 + "\n")
            log.write(f"[{datetime.utcnow()} UTC] SSH Login Attempt\n")
            log.write(f"IP: {self.client_ip}\n")
            log.write(f"Username: {username}\n")
            log.write(f"Password: {password}\n\n")
        return paramiko.AUTH_FAILED

def start_ssh_honeypot():
    host_key = paramiko.RSAKey.generate(2048)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", BIND_PORT))
    sock.listen(100)
    print(f"📡 SSH Honeypot listening on port {BIND_PORT}...")

    while True:
        client, addr = sock.accept()
        print(f"[+] Connection from {addr[0]}")

        transport = paramiko.Transport(client)
        try:
            transport.add_server_key(host_key)
            server = SSHServer(addr[0])
            transport.start_server(server=server)
            chan = transport.accept(5)
        except Exception as e:
            print(f"[!] SSH Error: {e}")
        finally:
            transport.close()

if __name__ == "__main__":
    start_ssh_honeypot()
