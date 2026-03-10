import yaml
import subprocess
import json
from datetime import datetime

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

host = config["proxmox_host"]
user = config["ssh_user"]
vms = config["vm_ids"]
containers = config["ct_ids"]

rapport_data = []
running_count = 0
stopped_count = 0

for vmid in vms:
    cmd = f"ssh {user}@{host} qm status {vmid}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    status = result.stdout.strip().replace("Status: ", "")

    if status == "status: running":
        running_count += 1
    else:
        stopped_count += 1
        
    rapport_data.append({"id":vmid, "typ": "VM", "Status": status, "node": host})
    print(f"Läst VM {vmid}: {status}")
    
        

for ctid in containers:
    cmd = f"ssh {user}@{host} pct status {ctid}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    status = result.stdout.strip().replace("Status: ", "")

    if status == "status: running":
        running_count += 1
    else:
        stopped_count += 1
        
    rapport_data.append({"id":ctid, "typ": "CT", "Status": status, "node": host})
    print(f"Läst CT {ctid}: {status}")

with open("rapport.json", "w") as json_file:
    json.dump(rapport_data, json_file, indent=4)

print(f"{running_count} Running, {stopped_count} Stopped")

nu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("inventory.log", "a") as log_file:
    log_file.write(f"[{nu}] Inventering körd: {running_count} running, {stopped_count} stopped.\n")
    