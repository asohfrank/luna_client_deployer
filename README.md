# Luna Client Deployer

This Python project automates the deployment and configuration of the Thales Luna Client on Windows systems. It performs:

- Silent installation of the Luna Client
- Client certificate generation via `vtl.exe`
- One-Step NTLS registration with Luna HSM (with verbose output)
- Logging of operations to `luna_client_deployer.log`

## Setup

1. Place your Luna Client installer executable in the `softwares/` directory or specify its path in `config.yaml`.
2. Place the Luna HSM server certificate file `server.pem` in the `dependencies/` directory or specify its location in `config.yaml`.
3. Update the `config.yaml` file with your environment parameters:
   - Luna Client install path
   - HSM server IP/hostname
   - Partition name and password
   - Optional: client certificate common name (hostname is used by default)

## Usage

Run the deployment script:

```bash
python main.py