# Find all python dependencies in all the scripts a folder (and subfolders)
import sys, os, io

MAX_DEPTH = 5 # max folder depth
PYTHON_EXTENSIONS = ['.py', '.pyw', '.py3']
PYTHON_STANDARD_MODULES = {'__future__', '__main__', '_thread', 'abc', 'aifc', 'argparse', 'array', 'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit', 'audioop', 'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser', 'contextlib', 'contextvars', 'copy', 'copyreg', 'cProfile', 'crypt', 'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'distutils', 'doctest', 'email', 'encodings', 'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch', 'formatter', 'fractions', 'ftplib', 'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob', 'graphlib', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 'msilib', 'msvcrt', 'multiprocessing', 'netrc', 'nis', 'nntplib', 'numbers', 'operator', 'optparse', 'os', 'ossaudiodev', 'parser', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib', 'poplib', 'posix', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'random', 're', 'readline', 'reprlib', 'resource', 'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex', 'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess', 'sunau', 'symbol', 'symtable', 'sys', 'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 'turtledemo', 'types', 'typing', 'unicodedata', 'unittest', 'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile', 'zipimport', 'zlib', 'zoneinfo'} # this lsit was definately not written manually. I love selenium !!!

def list_python_files(base_path, depth):
	# check if max depth has been reached
	if depth == 0:
		return []

	files = []
	os.chdir(base_path)
	for obj in os.listdir(base_path):
		# save some time
		if obj == '__pycache__':
			continue
		# full path
		obj = os.path.join(base_path, obj)
		# is file
		if os.path.isfile(obj):
			if any([obj.endswith(extension) for extension in PYTHON_EXTENSIONS]):
				files.append(obj)
		# is dir
		else:
			files.extend(list_python_files(obj, depth-1))

	os.chdir(base_path)
	return files

def is_local_module(file, module_name):
	path = os.path.dirname(file)
	return module_name + '.py' in os.listdir(path)

def find_dependencies(files):
	dependencies = []
	module_name = lambda dep: list(filter(None, dep.split()))[0].split('.')[0]

	for file in files:
		obj = io.open(file, mode='r', encoding='utf-8')
		lines = obj.readlines()
		obj.close()

		for line in lines:
			if line.startswith('import '):
				# worst case scenario: import numpy as np, tkinter.filedialog,pytorch
				for dep in line[7:].split(','):
					dep = module_name(dep)
					if dep and not is_local_module(file, dep):
						dependencies.append(
							dep
						)
			elif line.startswith('from '):
				# from os.path import isfile , isdir,dirname
				dep = module_name(line[5:])
				if dep and not is_local_module(file, dep):
					dependencies.append(
						dep
					)

	return dependencies

if __name__ == '__main__':
	assert sys.argv.__len__() == 2
	root_path = os.path.abspath(sys.argv[1])
	assert os.path.isdir(root_path)

	print('### AUTOMATIC DEPENDENCIES SEARCH (https://github.com/Nicolas-Reyland/list-py-modules)')
	python_files = list_python_files(root_path, MAX_DEPTH)
	dependencies = find_dependencies(python_files)
	dependencies = set(dependencies)
	# remove all std lib dependencies
	dependencies -= PYTHON_STANDARD_MODULES
	print('\n'.join(dependencies))
