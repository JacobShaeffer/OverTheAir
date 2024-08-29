import subprocess
import time

def measure_transfer_time(folder_path):
    print("folder_path: ", folder_path)

    # Define the destination base path
    remote_user = "pi"
    remote_host = "10.10.10.10"
    remote = f"{remote_user}@{remote_host}"
    test_path = f"~/test"
    base_path = f"pi@10.10.10.10:{test_path}"

    # Command to create necessary directories on the destination
    directory_setup_command = f"ssh {remote} 'rm -r {test_path}'"
    # Execute directory setup command
    subprocess.run(directory_setup_command, shell=True)

    directory_setup_command = f"ssh {remote} 'mkdir -p {test_path}/rsync'"
    subprocess.run(directory_setup_command, shell=True)

    # Commands to execute
    commands = [
        # f"rsync -az {folder_path} {base_path}/rsync/",
        # f"rsync -a {folder_path} {base_path}/rsync/",
        # f"rsync {folder_path}/* {base_path}/rsync/",
        # f"rsync --inplace {folder_path}/* {base_path}/rsync/",
        # f"rsync --inplace --no-compress {folder_path}/* {base_path}/rsync/",
        # f"rsync --inplace --trust-sender {folder_path}/* {base_path}/rsync/",
        # f"rsync --inplace --rsh=rsh {folder_path}/* {base_path}/rsync/",
        f"rsync --inplace --checksum-choice=auto,none {folder_path}/* {base_path}/rsync/",
    ]

    # Execute each command and measure the time taken
    for command in commands:
        print("current_command: ", command)
        start_time = time.time()
        subprocess.run(command, shell=True)
        end_time = time.time()
        print(f"{command}: {end_time - start_time:.2f}")

if __name__ == "__main__":
    # Example usage
    folder_path = "~/Downloads/overTheAirUpdate"
    measure_transfer_time(folder_path)
