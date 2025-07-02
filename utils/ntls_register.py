import subprocess
import os
import shutil
import sys
import socket
import threading
import itertools
import time

def spinner_task(stop_event):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        print('\r[*] Registering client with Luna HSM using NTLS... ' + next(spinner), end='', flush=True)
        time.sleep(0.2)
    print('\r[*] Registration complete!               ')

def deploy_client_config(luna_path, hsm_ip, partition_name, password, server_cert_path, client_name=None, username="admin"):
    # Verify server cert exists
    if not os.path.isfile(server_cert_path):
        print(f"[ERROR] Server certificate file not found: {server_cert_path}")
        print("Please place the server certificate file at the specified path in config.yaml and retry.")
        sys.exit(1)

    # Copy server cert to Luna Client cert/server folder
    cert_dir = os.path.join(luna_path, 'cert', 'server')
    os.makedirs(cert_dir, exist_ok=True)
    dest_cert_path = os.path.join(cert_dir, 'server.pem')
    shutil.copy(server_cert_path, dest_cert_path)
    print(f"[✔] Copied server certificate to: {dest_cert_path}")

    lunacm_path = os.path.join(luna_path, 'lunacm.exe')
    if not os.path.isfile(lunacm_path):
        print(f"[ERROR] lunacm.exe not found at: {lunacm_path}")
        sys.exit(1)

    client_name = client_name or socket.gethostname()

    command = [
        lunacm_path,
        '-q',
        'clientconfig',
        'deploy',
        '-server', hsm_ip,
        '-client', client_name,
        '-partition', partition_name,
        '-password', password,
        '-user', username,
        '-force'
    ]

    # Prepare a masked version for printing
    masked_command = command.copy()
    try:
        pw_index = masked_command.index('-password') + 1
        masked_command[pw_index] = '********'
    except ValueError:
        pass  # just in case '-password' not found

    print(f"[*] Running command: {' '.join(masked_command)}")

    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spinner_task, args=(stop_spinner,))
    spinner_thread.start()

    try:
        result = subprocess.run(command, capture_output=True, text=True)
    finally:
        stop_spinner.set()
        spinner_thread.join()

    print(f"\nstdout:\n{result.stdout}")
    print(f"stderr:\n{result.stderr}")

    if result.returncode != 0:
        print(f"[ERROR] lunacm command failed with exit code {result.returncode}")
        sys.exit(result.returncode)