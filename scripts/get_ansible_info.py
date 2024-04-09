import requests
import os
import shutil
import requests


def truncate_file_after_marker(file_path, marker):
    try:
        with open(file_path, 'r+') as file:
            lines = file.readlines()
            marker_index = -1

            # Find the marker line
            for i, line in enumerate(lines):
                if marker in line:
                    marker_index = i
                    break

            # If the marker line is found, truncate the file after that line
            if marker_index != -1:
                file.seek(0)
                file.truncate()
                file.writelines(lines[:marker_index+1])

        print(f"File '{file_path}' truncated after marker line '{marker}'")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def replace_text_in_file(file_path, old_text, new_text):
    # Read the content of the file
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Replace the old text with the new text
    modified_content = file_content.replace(old_text, new_text)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)

def et_phone_home(url):
    # Set your token
    TOKEN = "18a09ac581f3b2679df0f538698e2893aac493a7"    

    # Set the headers
    headers = {
        "Authorization": f"Token {TOKEN}",
        "Accept": "application/json; indent=4"
    }
    # Send the GET request
    response = requests.get(url, headers=headers)
    return response.json()

#define the terraform directory and empty the terraform configuration file
gitDir="/home/kevin/ansible"
truncate_file_after_marker(gitDir + '/main.tf', 'hosts:')

#gets a json object of all the vms
vms = et_phone_home("https://netbox.thejfk.ca/api/virtualization/virtual-machines/?limit=1000")

#iterates through the vms 
for vm in vms["results"]:    
    if vm["primary_ip4"] and vm["custom_fields"]['VMorContainer'][0] == "vm":                                                   
                                                                                   
        if vm['status']['value'] == 'active':
            
            #adds a line for each VM as a sub-module in the main module's configuration file             
            hostNameLine = "    " + vm["name"] + ":"
            hostIpLine = "      " + vm["primary_ip4"]["address"] + ":"
            with open(gitDir + '/inventory.yaml', 'a') as file:
                file.write(hostNameLine + '\n')   
                file.write(hostIpLine + '\n')   
            
                
                        