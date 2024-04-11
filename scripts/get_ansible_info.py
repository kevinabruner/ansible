import requests
import os
import shutil
import requests

def replace_text_in_file(file_path, old_text, new_text):
    # Read the content of the file
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Replace the old text with the new text
    modified_content = file_content.replace(old_text, new_text)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)

def write_with_indent(indent_level, text_to_write):
    indent_spaces = 2
    indent_text = " " * indent_level * indent_spaces
    
    with open(gitDir + '/inventory.yaml', 'a') as file:
        file.write(indent_text + text_to_write + '\n')   
    

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

#gets a json object of all the vms
vms = et_phone_home("https://netbox.thejfk.ca/api/virtualization/virtual-machines/?limit=1000")

#gets a list of all the repos/projects
repos_bulk = et_phone_home("https://netbox.thejfk.ca/api/extras/custom-field-choice-sets/?id=3")
repos = [couplet[0] for couplet in repos_bulk['results'][0]['extra_choices']]

#gets a list of all the workload stages (dev, prod, other)
stages_bulk = et_phone_home("https://netbox.thejfk.ca/api/extras/custom-field-choice-sets/?id=4")
stages = [couplet[0] for couplet in repos_bulk['results'][0]['extra_choices']]


shutil.copy(gitDir + '/inventory.template', gitDir + '/inventory.yaml')

for stage in stages:
    indent_level = 0
    write_with_indent(indent_level, stage + ":")   
    write_with_indent(1, "hosts:")      
                    
    #iterates through the vms 
    for vm in vms["results"]:    

        indent_level = 1

        if (
            vm['custom_fields']['VMorContainer'][0] == "vm" and
            vm['custom_fields']['repos'] == repo and
            vm['status']['value'] == 'active'
        ):      
                write_with_indent(indent_level + 1, vm["name"] + ":")
                write_with_indent(indent_level + 2, "ansible host: " + vm["primary_ip4"]["address"].split("/")[0])

for repo in repos:
    indent_level = 0
            
    write_with_indent(indent_level, repo + ":")   
    write_with_indent(1, "hosts:")      
                    
    #iterates through the vms 
    for vm in vms["results"]:    

        indent_level = 1

        if (
            vm['custom_fields']['VMorContainer'][0] == "vm" and
            vm['custom_fields']['repos'] == repo and
            vm['status']['value'] == 'active'
        ):      
                write_with_indent(indent_level + 1, vm["name"] + ":")
                write_with_indent(indent_level + 2, "ansible host: " + vm["primary_ip4"]["address"].split("/")[0])

                                