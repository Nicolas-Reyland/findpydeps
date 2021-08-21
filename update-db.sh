#!/bin/bash
wget -O - https://pypi.org/simple/ | awk '{print $2}' | cut -d '>' -f 2 | cut -d '<' -f 1 > pypi-pkgs.txt
