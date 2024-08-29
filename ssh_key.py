import subprocess
import os

def create_or_load_ssh_key(key_name, email):
    """Generate an SSH key pair if it doesn't exist, or use the existing one."""
    key_path = os.path.expanduser(f"~/.ssh/{key_name}")
    if not os.path.exists(key_path):
        subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-C", email, "-f", key_path, "-N", ""], check=True)
        print(f"SSH key generated at {key_path}")
        # Add to SSH config if a new key was created
        add_ssh_config(host, username, key_path)
        print("New SSH configuration added.")
    else:
        print(f"SSH key already exists at {key_path}")
    return key_path

def copy_ssh_key_to_host(public_key_path):
    """Copy the SSH public key to the specified host."""
    public_key = ""
    with open(public_key_path, "r") as file:
        public_key = file.read()
    command = f"echo {public_key.strip()} | ssh pi@10.10.10.10 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'"
    subprocess.run(command, shell=True, check=True)

def add_ssh_config(host, user, key_path):
    """Add an SSH config entry for the host."""
    config_path = os.path.expanduser("~/.ssh/config")
    with open(config_path, "a") as file:
        file.write(f"\nHost {host}\n")
        file.write(f"    HostName {host}\n")
        file.write(f"    User {user}\n")
        file.write(f"    IdentityFile {key_path}\n")

if __name__ == "__main__":
    # Fixed user and host information
    username = "pi"
    host = "10.10.10.10"
    key_name = input("Enter a name for your SSH key (e.g., id_rsa_test): ")
    email = input("Enter your email for the SSH key: ")

    # Create or load SSH key
    key_path = create_or_load_ssh_key(key_name, email)

    # Copy SSH key to remote host
    public_key_path = f"{key_path}.pub"
    try:
        copy_ssh_key_to_host(public_key_path)
        print("SSH key has been successfully copied to the remote host.")
    except subprocess.CalledProcessError:
        print("An error occurred while copying the SSH key to the remote host.")


