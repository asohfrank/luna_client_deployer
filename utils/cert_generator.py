import subprocess
import socket
import os

def generate_cert(luna_path, common_name=None):
    hostname = common_name or socket.gethostname()
    vtl_path = os.path.join(luna_path, "vtl.exe")
    subprocess.run([vtl_path, 'createCert', '-n', hostname], check=True)
