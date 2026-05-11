# File Description: Inventory helper for collecting Proxmox VM and container status.
# Author: Alhasan Al-Hmondi
# Version: 1.0.0

from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path

import yaml


CONFIG_PATH = Path("config.yaml")
REPORT_PATH = Path("rapport.json")
LOG_PATH = Path("inventory.log")


def load_config(path: Path) -> dict:
    """Load the YAML configuration used by the inventory script."""

    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def read_resource_status(user: str, host: str, command: str, resource_id: int) -> str:
    """Read VM or container status through SSH without invoking a shell."""

    result = subprocess.run(
        ["ssh", f"{user}@{host}", command, "status", str(resource_id)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    if result.returncode != 0:
        return f"error: {result.stderr.strip() or 'unknown error'}"

    return result.stdout.strip()


def collect_inventory(config: dict) -> tuple[list[dict], int, int]:
    """Collect configured VM and CT status rows from the Proxmox node."""

    host = config["proxmox_host"]
    user = config["ssh_user"]
    report_data: list[dict] = []
    running_count = 0
    stopped_count = 0

    resources = [
        ("VM", "qm", config.get("vm_ids", [])),
        ("CT", "pct", config.get("ct_ids", [])),
    ]

    for resource_type, command, resource_ids in resources:
        for resource_id in resource_ids:
            status = read_resource_status(user, host, command, resource_id)
            if status == "status: running":
                running_count += 1
            else:
                stopped_count += 1

            report_data.append(
                {"id": resource_id, "typ": resource_type, "Status": status, "node": host}
            )
            print(f"Läst {resource_type} {resource_id}: {status}")

    return report_data, running_count, stopped_count


def main() -> int:
    """Run inventory collection and write report artifacts."""

    config = load_config(CONFIG_PATH)
    report_data, running_count, stopped_count = collect_inventory(config)

    REPORT_PATH.write_text(json.dumps(report_data, indent=4), encoding="utf-8")
    print(f"{running_count} Running, {stopped_count} Stopped")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(
            f"[{timestamp}] Inventering körd: {running_count} running, "
            f"{stopped_count} stopped.\n"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
