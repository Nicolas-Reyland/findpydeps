# list-py-modules
Get a list of all the python dependencies in a folder (and its subfolders, etc.)

Example usage:
- python find-dependencies.py "C:\Documents\python\projects\"



The output can be redirected to a requirements.txt file, like this:
- python find-dependencies.py . > requirements.txt (where "." is the current directory)
- pip install -r requirements.txt

The dependencies are detected by reading all the python files in the directories.



There are some problems tho:
- imports have to be done at the beginning of lines in your python files (import .../from ... import ...)
- some dependencies have different names when you install them/when you use them. (e.g. import cv2 / pip install opencv-python)
- if you manually added your scripts into the sys.path or into the python library-folder, then import those scripts, they will be considered as dependencies (as opposed to local scripts, which are detected and not listed)
