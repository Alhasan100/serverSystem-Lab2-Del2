# ServerSystem Lab2 Del2

**Version:** 1.0.0 | **Author:** Alhasan Al-Hmondi

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

ServerSystem Lab2 Del2 is a small infrastructure automation lab for managing a Proxmox-based server environment. The project combines Python inventory reporting with Ansible desired-state automation so VM/CT status, firewall checks, and warning logs can be reviewed in a repeatable way.

## Why This Project Exists

I built this project as part of a server systems lab to practice practical infrastructure administration. The goal is not to create a large platform, but to show that I can document a lab environment, collect useful system state, run Ansible safely, and produce logs that are readable when something does not match the expected state.

## Stack

- Python 3
- PyYAML
- Ansible
- Proxmox CLI tools (`qm`, `pct`, `pve-firewall`)
- SSH key-based administration

## Project Parts

- **Del A:** Python inventory script that checks VM/CT status over SSH and writes `rapport.json` plus `inventory.log`.
- **Del B:** Ansible playbook that checks Proxmox state, starts expected machines, validates firewall status, and writes summary/warning logs.

## Project Structure

```text
serverSystem-Lab2-Del2/
|-- Del-A/
|   |-- Script.py
|   |-- config.yaml
|   |-- rapport.json
|   `-- inventory.log
|-- Del-B/
|   |-- Proxmox-Ansible/
|   |-- log.txt
|   `-- warning_log.txt
|-- LICENSE
|-- lab2_del2-dubai.pdf
`-- README.md
```

## Requirements

Run the automation from an Ansible admin host that can reach the Proxmox node over SSH.

Install the basic dependencies:

```bash
sudo apt update
sudo apt install ansible python3-yaml -y
```

Set up SSH key-based login to the Proxmox node:

```bash
ssh-keygen -t ed25519
ssh-copy-id root@<proxmox-node-ip>
ssh root@<proxmox-node-ip>
```

The repository uses documentation-safe example addresses such as `192.0.2.30`. Before running the lab, update:

- `Del-A/config.yaml`
- `Del-B/Proxmox-Ansible/inventory/hosts.ini`
- `Del-B/Proxmox-Ansible/group_vars/proxmox.yaml`

## Usage

Run the Python inventory:

```bash
cd Del-A
python3 Script.py
```

Run the Ansible desired-state playbook:

```bash
cd Del-B/Proxmox-Ansible
ansible-playbook playbook.yaml
```

Run a dry-run:

```bash
ansible-playbook playbook.yaml --check
```

Run a dry-run with diff output:

```bash
ansible-playbook playbook.yaml --check --diff
```

## What The Automation Checks

- VM and container status
- Expected running state for selected machines
- Firewall status on the Proxmox node
- Missing firewall allowance for the configured admin network
- Failed VM/CT start attempts

## Output Files

- `Del-A/rapport.json`: structured inventory output from the Python script
- `Del-A/inventory.log`: timestamped inventory run summary
- `Del-B/log.txt`: sample desired-state summary
- `Del-B/warning_log.txt`: sample warning output

## Final Scope

This project is intentionally focused on a small Proxmox lab. It demonstrates scripting, configuration management, SSH-based administration, desired-state thinking, warning handling, and operational documentation without hiding the actual infrastructure workflow behind a dashboard.

## Future Improvements

- Add an Ansible Vault example if credentials are ever needed
- Add CI validation for YAML syntax
- Add a sample `--check` output file for documentation
- Split environment-specific values into a clearer sample inventory

## License

This project is licensed under the GNU General Public License v3.0. See `LICENSE` for the full license text.
