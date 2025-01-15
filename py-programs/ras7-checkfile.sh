#!/bin/bash

for i in {1..12}; do
    # Define variables
    REMOTE_USER="alpha"
    REMOTE_HOST="172.16.17.220"
    REMOTE_FILE_PATH="/home/alpha/Documents/secret.dat"
    LOCAL_FILE_PATH="/home/alpha/Downloads/secret.dat"
    SSH_PASSWORD="hacker@123"
    EXPECTED_HASH="b2210a789ca49c8a627c8507b60571a6"
    HACKED_FILE="/home/alpha/hacked.txt"

    # Fetch the file using SCP
    sshpass -p "$SSH_PASSWORD" scp "$REMOTE_USER@$REMOTE_HOST:$REMOTE_FILE_PATH" "$LOCAL_FILE_PATH" >/dev/null 2>&1

    # Check if the file was fetched
    if [ -f "$LOCAL_FILE_PATH" ]; then
        # Calculate the MD5 hash of the downloaded file
        FILE_HASH=$(md5sum "$LOCAL_FILE_PATH" | awk '{ print $1 }')

        # Compare the hash with the expected hash
        if [ "$FILE_HASH" == "$EXPECTED_HASH" ]; then
            echo "false" > "$HACKED_FILE"   # Write "false" to hacked.txt if hash matches
        else
            echo "true" > "$HACKED_FILE"    # Write "true" to hacked.txt if hash doesn't match
        fi
    else
        # If the file wasn't fetched, consider the system hacked
        echo "true" > "$HACKED_FILE"
    fi

    sleep 5  # Wait 5 seconds before the next iteration
done
