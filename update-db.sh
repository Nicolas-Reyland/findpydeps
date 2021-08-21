#!/bin/bash
wget -O - https://pypi.org/simple/ | grep '<a href=' | awk '$2' | cut -d '>' -f 2 | cut -d '<' -f 1 | awk '$0 ~ /^[A-z_][A-z_0-9]*$/' | grep "\S" > pypi-module-list.txt
