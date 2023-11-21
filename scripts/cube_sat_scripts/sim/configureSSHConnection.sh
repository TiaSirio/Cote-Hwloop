#!/bin/bash

source simulation.conf

if [ "$#" -ne 6 ]; then
    echo "Invalid number of arguments. Usage: $1 <Desired SSH name>, $2 <HostName>, $3 <User of the Host>, $4 <Port>, $5 <SSH key name>, $6 <Password>"
    exit 1
fi

nameSSH=$1
address=$2
user=$3
port=$6
key_name=$5
password=$6

if grep -q "=${nameSSH}$" "$physicalSatelliteConf"; then
    echo "Satellite $nameSSH already exists in the conf file."
    exit 1
else
    # Find the last satellite number in the conf file
    last_satellite_number=$(grep -Eo "satellite[0-9]+" "$physicalSatelliteConf" | awk -F'satellite' '{print $2}' | sort -n | tail -1)

    # Increment the last satellite number by 1
    new_satellite_number=$((last_satellite_number + 1))

    # Append the new satellite entry to the conf file
    echo "satellite${new_satellite_number}=${nameSSH}" >> "$physicalSatelliteConf"
fi

# SSH directory
directory="$HOME/.ssh"
if [ -d "$directory" ]; then
  echo "SSH directory already exists"
else
  mkdir -p "$directory"
  chmod 700 "$directory"
  echo "Created SSH directory"
fi

# SSH config file
file="$HOME/.ssh/config"
if [ -e "$file" ]; then
  echo "Config file already exists"
else
  touch "$file"
  chmod 600 "$file"
  echo "Config file created"
fi

# SSH key generation
ssh-keygen -t rsa -N "$password" -f "$directory/$key_name"

# Writing on file
echo -e "\n Host $nameSSH\n\t HostName $address\n\t User $user\n\t IdentityFile $directory/$key_name\n" >> "$file"

# Copy public key
ssh-copy-id -i "$directory/$key_name.pub" "$nameSSH"

echo "SSH connection configured"
exit 0

