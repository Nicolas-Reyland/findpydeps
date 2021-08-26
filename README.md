# findpydeps
Find the python dependencies used by your python files and projects.

## Installation
Simply install it via pip:
```
pip install findpydeps
```

## Usage
For the usage, please refer to the `python3 -m findpydeps -h` output

Example usage:
```
python3 -m findpydeps -i "/home/$USER/python/example-project/" test.py ../test2.py
```

The output can be redirected to a requirements.txt file, like this:
```
python3 -m findpydeps -i . > requirements.txt
# or maybe a better alternative :
# python3 -m findpydeps -i main.py -l
# or (the same) :
# python3 -m findpydeps --input main.py --follow-local-imports
```
and then use the generated file:
```
python -m pip install -r requirements.txt
```
