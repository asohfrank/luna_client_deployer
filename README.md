# Luna Client Deployer

This Python project automates the deployment and configuration of the Thales Luna Client on Windows systems. It performs:

- Silent installation of Luna Client
- Client certificate generation via `vtl.exe`
- One-Step NTLS registration with Luna HSM

## Setup

1. Place your Luna Client installer executable in the `softwares/` directory or specify its path in `config.yaml`.
2. Place the Luna HSM server certificate file `server.pem` in the `dependencies/` directory or specify its location in `config.yaml`.
3. Update the `config.yaml` file with your environment parameters (Luna Client install path, HSM IP, partition name, passwords, etc.).

## Usage

Run the deployment script:

```bash
python main.py
