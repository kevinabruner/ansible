#!/usr/bin/env python3
import json
import requests
import subprocess
import os

# --- Configuration ---
NETBOX_URL = "https://netbox.thejfk.ca/api"
TOKEN = "18a09ac581f3b2679df0f538698e2893aac493a7"

def get_netbox_data(endpoint):
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Accept": "application/json"
    }
    response = requests.get(f"{NETBOX_URL}/{endpoint}", headers=headers)
    response.raise_for_status()
    return response.json()

def generate_inventory():

    inventory = {
        "_meta": {"hostvars": {}},
        "all": {"children": [TARGET_REPO, "dev", "prod"]},
        "dev": {"hosts": [], "vars": {}}, 
        "prod": {"hosts": [], "vars": {}} 
    }

    # Get VMs
    vms = get_netbox_data("virtualization/virtual-machines/")
    # Get IP Addresses
    ips = get_netbox_data("ipam/ip-addresses/")

    for vm in vms.get("results", []):
        custom_fields = vm.get('custom_fields', {})
        
        # 1. Logic Check: Must be 'active', a 'vm', and match our 'repo'
        is_active = vm.get('status', {}).get('value') == 'active'
        is_vm = custom_fields.get('VMorContainer') == ["vm"]
        is_correct_repo = custom_fields.get('repos') == TARGET_REPO

        if is_active and is_vm and is_correct_repo:
            vm_name = vm["name"]
            
            # 2. Extract Network Info
            raw_ip = vm.get("primary_ip4", {}).get("address", "").split("/")[0]
            
            if not raw_ip:
                continue

            # 3. Handle Environment Groups (dev/prod)
            env = custom_fields.get('dev_or_prod')
            if env:
                if env not in inventory:
                    inventory[env] = {"hosts": []}
                inventory[env]["hosts"].append(vm_name)

            # 4. Populate Host Variables (ansible_host)
            inventory["_meta"]["hostvars"][vm_name] = {
                "ansible_host": raw_ip,
                "netbox_id": vm["id"],
                "proxmox_vmid": custom_fields.get("vmid")
            }

    return inventory

if __name__ == "__main__":
    # Ansible expects JSON output to stdout
    print(json.dumps(generate_inventory(), indent=2))