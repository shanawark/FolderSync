import os
import shutil
import time
import argparse

def synchronize_folders(source_folder, replica_folder, log_file):
    # Ensure replica folder exists
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    # Get the list of files in source folder
    source_files = get_files_list(source_folder)
    replica_files = get_files_list(replica_folder)

    # Copy missing files from source to replica
    for file in source_files:
        if file not in replica_files:
            source_path = os.path.join(source_folder, file)
            replica_path = os.path.join(replica_folder, file)
            shutil.copy2(source_path, replica_path)
            log_action(log_file, f"Copied {file} to replica")

    # Remove extra files from replica
    for file in replica_files:
        if file not in source_files:
            replica_path = os.path.join(replica_folder, file)
            os.remove(replica_path)
            log_action(log_file, f"Removed {file} from replica")

    # Update contents of files in replica
    for file in source_files:
        source_path = os.path.join(source_folder, file)
        replica_path = os.path.join(replica_folder, file)
        try:
            with open(source_path, 'rb') as f_source:
                content_source = f_source.read()
            with open(replica_path, 'wb') as f_replica:
                f_replica.write(content_source)
            log_action(log_file, f"Updated {file} in replica")
        except IOError:
            log_action(log_file, f"Failed to update {file} in replica (binary file)")

def get_files_list(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

def log_action(log_file, message):
    with open(log_file, 'a') as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f.write(f"{timestamp}: {message}\n")
    print(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Folder synchronization')
    parser.add_argument('source_folder', type=str, help='Path to source folder')
    parser.add_argument('replica_folder', type=str, help='Path to replica folder')
    parser.add_argument('log_file', type=str, help='Path to log file')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    args = parser.parse_args()

    while True:
        synchronize_folders(args.source_folder, args.replica_folder, args.log_file)
        time.sleep(args.interval)
