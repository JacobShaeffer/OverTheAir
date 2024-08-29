import subprocess
import shutil

def rsync_transfer(pack_location, progress_callback):
    # Define destination settings
    user_host = "pi@10.10.10.10"
    base_destination = "/var/www/html"

    # Define the subdirectory paths
    content_source = f"{pack_location}/content/*"
    db_source = f"{pack_location}/db/solarspell_test.db"
    modules_source = f"{pack_location}/modules/*"

    # Define the target paths on the destination
    content_destination = f"{user_host}:{base_destination}/content"
    db_destination = f"{user_host}:{base_destination}/backend/solarspell_test.db"
    modules_destination = f"{user_host}:{base_destination}"

    rsync_path = shutil.which("rsync")

    # Transfer the 'content' folder
    progress_callback("Starting transfer of content files...")
    command = f"{rsync_path} --inplace --info=progress2 {content_source} {content_destination}"
    run_command(command, progress_callback)

    progress_callback("database")

    # # Transfer the 'db' folder
    # progress_callback("Starting transfer of database files...")
    # command = f"{rsync_path} -v --info=progress2 {db_source} {db_destination}"
    # run_command(command, progress_callback)

    # # Transfer the 'modules' folder
    # progress_callback("Starting transfer of module directories...")
    # command = f"{rsync_path} -av --info=progress2 {modules_source} {modules_destination}"
    # run_command(command, progress_callback)

def run_command(command, progress_callback):
    print(command)
    """ Run rsync command with progress update. """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            progress_callback(output.strip())

    rc = process.poll()
    return rc

# Example callback function to handle the progress updates
def progress_update(message):
    print(message)

# Example usage
if __name__ == "__main__":
    pack_location = "/Users/jacob/Documents/scratch/OverTheAir/test1pack"
    rsync_transfer(pack_location, progress_update)
    print("done")
