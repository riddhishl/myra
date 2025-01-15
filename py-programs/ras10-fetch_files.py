import paramiko
import os

# SCP details
remote_host = '172.16.17.202'
remote_user = 'alpha'
remote_password = 'hacker@123'
remote_path = '/home/alpha/approvedFiles'
local_path = '/home/alpha/Ads'

def fetch_files_via_scp():
    try:
        # SSH connection setup
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_host, username=remote_user, password=remote_password)

        # SCP setup
        sftp = ssh.open_sftp()

        # Fetch remote files
        remote_files = sftp.listdir(remote_path)

        if not remote_files:
            print("No new files fetched. Keeping existing files in the Ads folder.")
        else:
            # Clear local Ads folder before copying new files
            for local_file in os.listdir(local_path):
                local_file_path = os.path.join(local_path, local_file)
                os.remove(local_file_path)

            # Download each file from remote to local directory
            for file_name in remote_files:
                remote_file_path = os.path.join(remote_path, file_name)
                local_file_path = os.path.join(local_path, file_name)
                sftp.get(remote_file_path, local_file_path)
                print(f"Fetched and saved {file_name} to {local_file_path}")

        # Close connections
        sftp.close()
        ssh.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the fetch function
fetch_files_via_scp()
