#!/bin/bash

# check for root privs
if [ "$EUID" -ne 0 ]; then
	echo "/!\\ This script must be run as root /!\\"
	exit 1
fi

# check for python3 installation
if ! [ -x "$(command -v python3)" ]; then
	echo "/!\\ Python 3 is not installed /!\\"
	exit 1
fi

# get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# add to /usr/local/bini
src_path="$SCRIPT_DIR/find-py-dependencies.py"
dest_path="/usr/local/bin/find-py-dependencies"

add_script_to_path () {
	ln $src_path $dest_path &> /dev/null || cp $src_path $dest_path
}

if [ -f $dest_path ]; then
	echo -n "The file \"$dest_path\" already exists. Overwrite [yes/*] ? "
	read answer
	if [ "$answer" != "yes" ]; then
		echo "Operation cancelled"
		exit
	fi
fi

add_script_to_path

