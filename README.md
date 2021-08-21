# find-py-dependencies
Find the python dependencies used by a python file.

## Installation (for advanced usage only)

Run the pypi module list update script:
```
./update-pypi-list.sh
```

Alternatively, run this:
```
wget -O - https://pypi.org/simple/ | grep '<a href=' | awk '$2' | cut -d '>' -f 2 | cut -d '<' -f 1 | awk '$0 ~ /^[A-z_][A-z_0-9]*$/' | grep "\S" > pypi-module-list.txt
```

Example usage:
```
python find-py-dependencies.py -i "/home/$USER/python/example-project/" test.py ../test2.py
```


The output can be redirected to a requirements.txt file, like this:
```
./find-py-dependencies.py -i . > requirements.txt
# or maybe a better alternative :
# ./find-py-dependencies.py -i main.py -l
# or (the same) :
# ./find-py-dependencies.py --input main.py --follow-local-imports
```
and then use the generated file:
```
python -m pip install -r requirements.txt
```

The dependencies are detected by reading all the python files in the directories.
The maximum recursive folder-depth is manually set to 5 (see source code -> *consts declared at the top of the script*). The "\_\_pycache__" folders are not looked into.


There are some flaws tho:
- imports have to be done at the beginning of lines in your python files (import .../from ... import ...)
- some dependencies have different names when you install them/when you use them. (e.g. import cv2 / pip install opencv-python)
- if you manually added your scripts to the sys.path or pasted them to the python library-folder and import those scripts, they will be considered as dependencies (as opposed to local scripts, which are detected and not listed)
