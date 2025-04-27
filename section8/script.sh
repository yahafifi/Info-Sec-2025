#!/bin/bash

# Check if the user passed an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 keyword"
    exit 1
fi

keyword=$1  # the keyword passed from command line

# Step 1: Extract URLs containing the keyword
cat index.html | grep "href=" | cut -d "/" -f 3 | grep "\." | cut -d '"' -f 1 | sort -u | grep "$keyword" > url.txt

# Step 2: Loop through the URLs and resolve IPs
> ips.txt  # Clear ips.txt before writing
for url in $(cat url.txt)
do
    host $url | grep "has address" | cut -d " " -f 4 >> ips.txt
done

# Step 3: Show the collected IPs
cat ips.txt
