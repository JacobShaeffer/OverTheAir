import paramiko
import os

def sftp_transfer(sftp, local_path, remote_path, progress_callback):
    total_size = 0
    transferred_size = 0

    # Calculate total size of files to be transferred
    if os.path.isdir(local_path):
        for root, _, files in os.walk(local_path):
            for file in files:
                total_size += os.path.getsize(os.path.join(root, file))
    else:
        total_size = os.path.getsize(local_path)

    def progress_report(transferred, total):
        percentage = (transferred / total) * 100
        progress_callback(percentage)

    def transfer_file(local_file, remote_file):
        nonlocal transferred_size
        sftp.put(local_file, remote_file, callback=lambda sent, total: progress_report(transferred_size + sent, total_size))
        transferred_size += os.path.getsize(local_file)

    if os.path.isdir(local_path):
        for root, _, files in os.walk(local_path):
            for file in files:
                local_file = os.path.join(root, file)
                relative_path = os.path.relpath(local_file, local_path)
                remote_file = os.path.join(remote_path, relative_path).replace("\\", "/")
                remote_dir = os.path.dirname(remote_file)
                
                try:
                    sftp.stat(remote_dir)
                except FileNotFoundError:
                    sftp.mkdir(remote_dir)
                
                transfer_file(local_file, remote_file)
    else:
        transfer_file(local_path, remote_path)

def pack_transfer(pack_location, progress_callback):
    # Define destination settings
    user_host = "pi@10.10.10.10"
    base_destination = "/var/www/html"
    username, hostname = user_host.split('@')

    # Define the subdirectory paths
    content_source = f"{pack_location}/content"
    db_source = f"{pack_location}/db/solarspell_test.db"
    modules_source = f"{pack_location}/modules"

    # Define the target paths on the destination
    content_destination = f"{base_destination}/content"
    db_destination = f"{base_destination}/backend/solarspell_test.db"
    modules_destination = f"{base_destination}"

    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username)

    # Open SFTP session
    sftp = ssh.open_sftp()

    try:
        # Transfer the 'content' folder
        progress_callback("Starting transfer of content files...")
        sftp_transfer(sftp, content_source, content_destination, progress_callback)

        # Transfer the database file
        progress_callback("Starting transfer of database file...")
        sftp_transfer(sftp, db_source, db_destination, progress_callback)

        # Transfer the 'modules' folder
        progress_callback("Starting transfer of modules files...")
        sftp_transfer(sftp, modules_source, modules_destination, progress_callback)
    finally:
        sftp.close()
        ssh.close()

    progress_callback("Transfer complete.")