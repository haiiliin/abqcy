# Getting Started

`abqcy` allows you to write your Abaqus subroutines in [Cython](https://cython.org/).
It provides a command line tool to compile your Cython code into an object file (`.obj`) that can be used by Abaqus.

## Installation

You can install `abqcy` with `pip`:
```shell
pip install abqcy
```
or install it from source:
```shell
pip install git+https://github.com/haiiliin/abqcy
```

## Environment Setup

`abqcy` requires a working Abaqus installation with user subroutines enabled.
Make sure the `abaqus` command is available in the command line, otherwise you need to create a new system environment
variable `ABAQUS_BAT_PATH` and set it to the path of the `abaqus.bat` file.

`abqcy` uses [Cython](https://cython.org/) to compile your Cython code into a C source file (`.c`).
In order to compile the C source file into an object file (`.obj`) that can be used by Abaqus, the `abaqus make` command
is used (it uses the MSVC `cl`).
Since the compiled `.c` file requires the Python headers and libraries, `abqcy` will try to find them automatically and
set update the `INCLUDE` and `LIB` environment variables.

## Usage

You can now write your Abaqus subroutine in Cython, simple scripts can be found in {doc}`examples`.

```{note}
In order to not mess up with the Cython declarations, you can add a companion `.pxd` file with the same name as your
Cython `.py` or `.pyx` file, and put the Cython declarations in it.
If you are not comfortable with keeping two files, you can just use the `.pyx` file with the Cython declarations.

 See {doc}`examples` for detailed examples.
```

After you have written your subroutine, you can compile it with the `abqcy` command:
```shell
abqcy compile <path-to-your-subroutine>
```
This will compile your subroutine into a C source file (`.c`) and a C header file (`.h`), and then they will be compiled into an object file (`.obj`)
that can be used by Abaqus. These files are in the same directory as your subroutine.

Now you can use the subroutine in Abaqus, like:
```shell
abaqus job=Job-1 input=model.inp user=your-subroutine.obj
```
