import subprocess
import os
import shutil
import sys
import socket
import threading
import itertools
import time
import logging

# Configure logging
LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'luna_client_deployer.log'))
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
)

def spinner_task(stop_event):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        print('\r[*] Registering client with Luna HSM using NTLS... ' + next(spinner), end='', flush=True)
        time.sleep(0.2)
    print('\r[*] Registration complete!               ')

def deploy_client_config(luna_path, hsm_ip, partition_name, password, server_cert_path, client_name=None, username="admin"):
    logging.info("Starting NTLS registration")

    # Verify server cert exists
    if not os.path.isfile(server_cert_path):
        error_msg = f"Server certificate file not found: {server_cert_path}"
        logging.error(error_msg)
        print(f"[ERROR] {error_msg}")
        sys.exit(1)

    # Copy server cert to Luna Client cert/server folder
    cert_dir = os.path.join(luna_path, 'cert', 'server')
    os.makedirs(cert_dir, exist_ok=True)
    dest_cert_path = os.path.join(cert_dir, 'server.pem')
    shutil.copy(server_cert_path, dest_cert_path)
    print(f"[✔] Copied server certificate to: {dest_cert_path}")
    logging.info(f"Copied server certificate from {server_cert_path} to {dest_cert_path}")

    lunacm_path = os.path.join(luna_path, 'lunacm.exe')
    if not os.path.isfile(lunacm_path):
        error_msg = f"lunacm.exe not found at: {lunacm_path}"
        logging.error(error_msg)
        print(f"[ERROR] {error_msg}")
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
        '-force',
        '-verbose'
    ]

    print(f"[*] Running command: NTLS clientconfig")
    logging.info(f"Running NTLS registration command: {' '.join(command)}")

    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spinner_task, args=(stop_spinner,))
    spinner_thread.start()

    try:
        result = subprocess.run(command, capture_output=True, text=True)
    finally:
        stop_spinner.set()
        spinner_thread.join()

    logging.info("NTLS command stdout:\n" + result.stdout.strip())
    logging.info("NTLS command stderr:\n" + result.stderr.strip())

    print(f"\nstdout:\n{result.stdout}")
