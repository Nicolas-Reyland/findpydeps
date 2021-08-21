#!/usr/bin/env python3
from __future__ import annotations

# Find Python Dependencies
from argparse import ArgumentParser
import os, fnmatch
import ast


# - Setup the Argument Parser -
parser = ArgumentParser(
    description="Find the python dependencies used by your projects"
)

parser.add_argument(
    "-i",
    "--input",
    metavar="input",
    type=str,
    nargs="+",
    help="input files and/or directories (directories will be scanned for *.py files)",
)

parser.add_argument(
    "-d",
    "--dir-scanning-expr",
    metavar="expr",
    type=str,
    default="*.py",
    help="only process files with this expression in scanned directories [default: %(default)s]",
)

parser.add_argument(
    "-r",
    "--removal-policy",
    metavar="policy",
    type=int,
    default=0,
    help="removal policy for modules (0: local & stdlib, 1: local only, 2: stdlib only, 3: no removal) [default: %(default)s]",
)

parser.add_argument(
    "-l",
    "--follow-local-imports",
    action="store_true",
    help="follow imports for local files",
)

parser.add_argument(
    "-s",
    "--strict",
    action="store_true",
    help="raise an error on syntaxerrors in the input python files",
)

parser.add_argument(
    "--blocks",
    dest="blocks",
    action="store_true",
    help="scan contents of 'if', 'try' and 'with' blocks",
)

parser.add_argument(
    "--no-blocks",
    dest="blocks",
    action="store_false",
    help="don't scan contents of 'if', 'try' and 'with' blocks",
)

parser.set_defaults(blocks=True)

parser.add_argument(
    "--functions",
    dest="functions",
    action="store_true",
    help="scan contents of functions",
)

parser.add_argument(
    "--no-functions",
    dest="functions",
    action="store_false",
    help="don't scan contents of functions",
)

parser.set_defaults(functions=True)

parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="verbose mode (all messages prepended with '#')",
)

parser.add_argument(
    "--header", dest="header", action="store_true", help="show the project header"
)

parser.add_argument(
    "--no-header",
    dest="header",
    action="store_false",
    help="don't show the project header",
)

parser.set_defaults(header=True)


# - Setup Constants & Functions -
HEADER: str = "# Generated by https://github.com/Nicolas-Reyland/find-py-dependencies"

PYTHON_STANDARD_MODULES: set[str] = {
    "__future__",
    "__main__",
    "_thread",
    "abc",
    "aifc",
    "argparse",
    "array",
    "ast",
    "asynchat",
    "asyncio",
    "asyncore",
    "atexit",
    "audioop",
    "base64",
    "bdb",
    "binascii",
    "binhex",
    "bisect",
    "builtins",
    "bz2",
    "calendar",
    "cgi",
    "cgitb",
    "chunk",
    "cmath",
    "cmd",
    "code",
    "codecs",
    "codeop",
    "collections",
    "colorsys",
    "compileall",
    "concurrent",
    "configparser",
    "contextlib",
    "contextvars",
    "copy",
    "copyreg",
    "cProfile",
    "crypt",
    "csv",
    "ctypes",
    "curses",
    "dataclasses",
    "datetime",
    "dbm",
    "decimal",
    "difflib",
    "dis",
    "distutils",
    "doctest",
    "email",
    "encodings",
    "ensurepip",
    "enum",
    "errno",
    "faulthandler",
    "fcntl",
    "filecmp",
    "fileinput",
    "fnmatch",
    "formatter",
    "fractions",
    "ftplib",
    "functools",
    "gc",
    "getopt",
    "getpass",
    "gettext",
    "glob",
    "graphlib",
    "grp",
    "gzip",
    "hashlib",
    "heapq",
    "hmac",
    "html",
    "http",
    "imaplib",
    "imghdr",
    "imp",
    "importlib",
    "inspect",
    "io",
    "ipaddress",
    "itertools",
    "json",
    "keyword",
    "lib2to3",
    "linecache",
    "locale",
    "logging",
    "lzma",
    "mailbox",
    "mailcap",
    "marshal",
    "math",
    "mimetypes",
    "mmap",
    "modulefinder",
    "msilib",
    "msvcrt",
    "multiprocessing",
    "netrc",
    "nis",
    "nntplib",
    "numbers",
    "operator",
    "optparse",
    "os",
    "ossaudiodev",
    "parser",
    "pathlib",
    "pdb",
    "pickle",
    "pickletools",
    "pipes",
    "pkgutil",
    "platform",
    "plistlib",
    "poplib",
    "posix",
    "pprint",
    "profile",
    "pstats",
    "pty",
    "pwd",
    "py_compile",
    "pyclbr",
    "pydoc",
    "queue",
    "quopri",
    "random",
    "re",
    "readline",
    "reprlib",
    "resource",
    "rlcompleter",
    "runpy",
    "sched",
    "secrets",
    "select",
    "selectors",
    "shelve",
    "shlex",
    "shutil",
    "signal",
    "site",
    "smtpd",
    "smtplib",
    "sndhdr",
    "socket",
    "socketserver",
    "spwd",
    "sqlite3",
    "ssl",
    "stat",
    "statistics",
    "string",
    "stringprep",
    "struct",
    "subprocess",
    "sunau",
    "symbol",
    "symtable",
    "sys",
    "sysconfig",
    "syslog",
    "tabnanny",
    "tarfile",
    "telnetlib",
    "tempfile",
    "termios",
    "test",
    "textwrap",
    "threading",
    "time",
    "timeit",
    "tkinter",
    "token",
    "tokenize",
    "trace",
    "traceback",
    "tracemalloc",
    "tty",
    "turtle",
    "turtledemo",
    "types",
    "typing",
    "unicodedata",
    "unittest",
    "urllib",
    "uu",
    "uuid",
    "venv",
    "warnings",
    "wave",
    "weakref",
    "webbrowser",
    "winreg",
    "winsound",
    "wsgiref",
    "xdrlib",
    "xml",
    "xmlrpc",
    "zipapp",
    "zipfile",
    "zipimport",
    "zlib",
    "zoneinfo",
}  # this set was definately not written manually. I love selenium !!!

DEPENDENCIES: set[str] = set()
READ_FILES: set[str] = set()

vprint = lambda *a, **k: None


get_module_name = lambda s: s.split(".")[0]

def parse_input_file(input_file: str) -> ast.AST:
    global vprint

    with open(input_file, "r") as file:
        content = file.read()
        try:
            as_tree: ast.AST = ast.parse(content)
        except SyntaxError as se:
            vprint(f"Failed: {se}")
            return None

    return as_tree


def modules_from_ast_import_object(obj: ast.Import | ast.ImportFrom) -> set[str]:
    global vprint

    T = type(obj)
    if T is ast.ImportFrom:
        if obj.level != 0 and remove_local_imports:
            return set()
        if obj.module:
            return {get_module_name(obj.module)}
        return set()
    assert T is ast.Import
    return set(map(lambda name: get_module_name(name.name), obj.names))


def handle_ast_object(obj: ast.AST, blocks: bool, functions: bool) -> set[str]:
    global vprint

    T = type(obj)
    assert issubclass(T, ast.AST)

    if not blocks and T in [ast.If, ast.With, ast.Try]:
        return set()
    if not functions and T is ast.FunctionDef:
        return set()

    if T in [ast.Import, ast.ImportFrom]:
        modules = modules_from_ast_import_object(obj)
        vprint(f"Modules found: {modules}")
        return modules

    modules: set[str] = set()
    for attr_name, attr_value in filter(
        lambda key_value: not key_value[0].startswith("_"), obj.__dict__.items()
    ):
        if (
            attr_value
            and type(attr_value) is list
            and issubclass(type(attr_value[0]), ast.AST)
        ):
            for sub_obj in attr_value:
                modules |= handle_ast_object(sub_obj, blocks, functions)
    return modules


def find_file_dependencies(
    input_file: str,
    as_tree: ast.AST,
    blocks: bool,
    functions: bool,
    remove_local_imports: bool,
    follow_local_imports: bool,
) -> set[str]:
    global READ_FILES, vprint

    # assert this so we know the path is unique
    assert os.path.isabs(input_file)

    # add file to the read files
    if input_file in READ_FILES:
        return set()
    READ_FILES.add(input_file)

    dirpath = os.path.dirname(input_file)
    local_dependencies = handle_ast_object(as_tree, blocks, functions)

    # remove local imports || following local imports
    if remove_local_imports or follow_local_imports:
        for local_file in filter(os.path.isfile, map(lambda fn: os.path.join(dirpath, fn), os.listdir(dirpath))):
            file_name = os.path.basename(local_file)
            vprint(f"filename: {file_name}")

            if file_name.endswith(".py"):
                file_module_name = file_name[:-3]
            elif file_name.endswith(".py3"):
                file_module_name = file_name[:-4]
            elif file_name.endswith(".pyw"):
                file_module_name = file_name[:-4]
            else:  # not a python file
                continue

            # not interested in file
            if file_module_name not in local_dependencies:
                continue

            # remove local imports
            if remove_local_imports:
                vprint(f"removing local import: {file_module_name}")
                local_dependencies.remove(file_module_name)

            # follow local import
            if follow_local_imports and (as_tree := parse_input_file(local_file)):
                vprint(f"following local import: {file_module_name}")
                local_dependencies |= find_file_dependencies(local_file, as_tree, blocks, functions, remove_local_imports, follow_local_imports)

    return local_dependencies


# - Main function -
def main():
    global DEPENDENCIES, vprint

    # parse the command line arguments
    args = vars(parser.parse_args())

    # assert input was given
    if not args["input"]:
        raise ValueError(f'Missing argument "input" (-i/--input)')

    # validate removal policy
    if args["removal_policy"] < 0 or args["removal_policy"] > 3:
        raise ValueError(f'Invalid removal policy: {args["removal_policy"]}')

    # get values from args
    remove_local_imports = args["removal_policy"] < 2

    # init files & directories
    input_files = list()
    input_directories = list()

    # evaluate the paths & check their existence
    for rel_path in args["input"]:
        abs_path = os.path.abspath(rel_path)
        if not os.path.exists(abs_path):
            raise OSError(f'Input path: "{abs_path}" does not exist')
        if os.path.isfile(abs_path):
            input_files.append(abs_path)
        elif os.path.isdir(abs_path):
            input_directories.append(abs_path)
        else:
            raise OSError(f'Unhandeled object at "{abs_path}"')

    # scan the folders
    for folder in input_directories:
        for path, _, files in os.walk(folder):
            filtered_files = fnmatch.filter(files, args["dir_scanning_expr"])
            input_files.extend(map(lambda fn: os.path.join(path, fn), filtered_files))

    # print the header if asked for (default behaviour)
    if args["header"]:
        global HEADER
        print(HEADER)

    # setup verbose print function
    if args["verbose"]:
        vprint = lambda *a, **k: print("#", *a, **k)

        vprint()
        vprint("verbose mode")
        vprint(f"params: {args}")

    # parse the input files into abstract syntax trees
    vprint()
    vprint("Parsing the files ...")

    file_path_tree_pairs: list[tuple[str & ast.AST]] = list()
    for input_file in input_files:
        vprint(f'Parsing tree for: "{input_file}"')
        if as_tree := parse_input_file(input_file):
            file_path_tree_pairs.append((input_file, as_tree))

    vprint()
    vprint("Searching for imports ...")

    # add all the dependency-sets
    num_pairs = len(file_path_tree_pairs)
    for i in range(num_pairs):
        vprint(f"Doing AST {i+1}/{num_pairs}")
        file_path, as_tree = file_path_tree_pairs[i]
        DEPENDENCIES |= find_file_dependencies(file_path, as_tree, args["blocks"], args["functions"], remove_local_imports, args["follow_local_imports"])

    # remove the python stdlib dependencies ?
    if args["removal_policy"] % 2 == 0:
        vprint("Removing imports from the python stdlib")
        global PYTHON_STANDARD_MODULES
        DEPENDENCIES -= PYTHON_STANDARD_MODULES

    # finally output the content of the dependencies
    vprint()
    vprint("Done. Printing the module names")

    for dep in list(DEPENDENCIES):
        print(dep)


if __name__ == "__main__":
    main()