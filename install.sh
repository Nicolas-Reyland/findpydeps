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

# add to /usr/local/bin
ln -s "$SCRIPT_DIR/find-py-dependencies.py" "/usr/local/bin/find-py-dependencies"

