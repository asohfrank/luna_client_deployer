import os
import logging
from utils import installer, cert_generator, ntls_register, dependency_check

# Configure logging
log_file = os.path.join(os.path.dirname(__file__), "luna_client_deployer.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def main():
    dependency_check.ensure_dependencies()

    import yaml
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    luna_path = config["luna_client"].get("install_dir", "C:\\Program Files\\SafeNet\\LunaClient")
    installer_path = config["luna_client"].get("installer_path", "softwares/LunaClientInstaller.exe")
    install_args = config["luna_client"]["install_args"]

    # Install Luna Client if not installed
    if not os.path.isdir(luna_path):
        installer.install_luna_client(installer_path, install_args, luna_path)
    else:
        print(f"[✔] Luna Client already installed at: {luna_path}")
        logger.info(f"Luna Client already installed at: {luna_path}")

    hostname = config["cert"].get("common_name")
    cert_generator.generate_cert(luna_path, hostname)

    ntls = config["ntls"]
    ntls_register.deploy_client_config(
        luna_path,
        ntls["hsm_ip"],
        ntls["partition_name"],
        ntls["partition_password"],
        ntls["server_cert_path"],
        client_name=ntls.get("client_name"),
        username=ntls.get("username", "admin")
    )

if __name__ == "__main__":
    main()