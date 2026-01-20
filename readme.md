# Ansible
This controls all my software. 

# .bashrc
Put this at the end, or you'll never access the inventory token
```
VAULT_PATH="/home/kevin/ansible/vault.yaml"
PASS_PATH="/home/kevin/.vaultpass"

if [ -f "$VAULT_PATH" ] && [ -f "$PASS_PATH" ]; then
    # Extracts the value after the colon, then strips quotes and whitespace
    TOKEN=$(ansible-vault view "$VAULT_PATH" --vault-password-file "$PASS_PATH" | awk -F': ' '/netbox_token/ {print $2}' | tr -d '"' | tr -d "'" | xargs)
    if [ -n "$TOKEN" ]; then
        export NETBOX_API_TOKEN="$TOKEN"
    fi
fi
```
# vault pass
Create a vault pass at `/home/kevin/.vaultpass`. Just the password by itself in the file. 600 permissions.
If you don't know the password, oops!
