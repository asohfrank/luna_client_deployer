# File: utils/installer.py
import subprocess
import os

def install_luna_client(installer_path, install_args, install_dir):
    lunacm_path = os.path.join(install_dir, "lunacm.exe")

    if os.path.exists(lunacm_path):
        print(f"[✔] Luna Client already installed at: {install_dir}")
        return

    print("[*] Installing Luna Client...")
    try:
        subprocess.run([installer_path] + install_args.split(), check=True)
        print("[✔] Luna Client installation completed.")
    except subprocess.CalledProcessError as e:
        print("[!] Luna Client installation failed.")
        raise e
