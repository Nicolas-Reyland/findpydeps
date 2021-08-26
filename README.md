# find-py-dependencies
Find the python dependencies used by your python files and projects.

For the usage, please refer to the `./find-py-dependencies.py -h` output

Example usage:
```
./find-py-dependencies.py -i "/home/$USER/python/example-project/" test.py ../test2.py
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
