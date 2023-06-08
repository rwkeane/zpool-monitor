import sys
import re
import json

def ExtractJson(zpool_status):
    # Initialize variables
    tables = []
    current_table = None
    in_table = False

    # Read the input line by line
    for line in sys.stdin:
        # Check if the line contains the table column names
        if re.match(r"\s+NAME\s+STATE\s+READ\s+WRITE\s+CKSUM", line):
            # Create a new table
            in_table = True
            continue

        # Check if the line is empty (end of the table)
        if not line.strip():
            if current_table is not None:
                tables.append(current_table)
                current_table = None
            in_table = False
            continue

        # Check if the line contains the device information
        if in_table:
            matches = \
                re.match(r"\s+(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)", line)
            if not matches:
                continue
                
            # Extract the device information
            device_info = {
                "name": matches.group(1),
                "state": matches.group(2),
                "read": int(matches.group(3)),
                "write": int(matches.group(4)),
                "cksum": int(matches.group(5))
            }
            
            print(device_info["name"])
            if current_table is None:
                device_info["vdevs"] = []
                current_table = device_info
                continue
                
            if device_info["name"].startswith("raidz"):
                device_info["devices"] = []
                current_table["vdevs"].append(device_info)
                continue
                
            current_table["vdevs"][-1]["devices"].append(device_info)

    # Generate the output dictionary
    output = {"tables": tables}

    # Convert the output to JSON
    json_output = json.dumps(output, indent=2)

    # Print the resulting JSON
    return json_output
