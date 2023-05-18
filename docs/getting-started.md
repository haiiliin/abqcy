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
is used (it uses the MSVC `cl` compiler from Visual Studio). Since the compiled `.c` file requires the Python headers and
libraries, you need to make sure that the `cl` compiler can find them. This can be done by setting the `INCLUDE` and
`LIB` environment variables. If you do not want to set
global environment variables, you can also create a `.env` file in the directory where you run the `abqcy` command.

The following is the information of the `INCLUDE`environment variable on my computer, you need to separate
the paths with `;` on Windows and `:` on Linux:
```shell
C:/Users/Hailin/AppData/Local/Programs/Python/Python310/include
C:/Users/Hailin/AppData/Local/Programs/Python/Python310/Lib/site-packages/numpy/core/include
C:/Program Files (x86)/Microsoft Visual Studio/2019/BuildTools/VC/Tools/MSVC/14.29.30133/include
C:/Program Files (x86)/Windows Kits/10/Include/10.0.19041.0/shared
C:/Program Files (x86)/Windows Kits/10/Include/10.0.19041.0/ucrt
```
and the following is the information of the `LIB` environment variable on my computer:
```shell
C:/Users/Hailin/AppData/Local/Programs/Python/Python310/libs
C:/Users/Hailin/AppData/Local/Programs/Python/Python310/Lib/site-packages/numpy/core/lib
C:/Program Files (x86)/Windows Kits/10/Lib/10.0.19041.0/um/x64
C:/Program Files (x86)/Windows Kits/10/Lib/10.0.19041.0/ucrt/x64
```

## Usage

You can now write your Abaqus subroutine in Cython, simple scripts can be found in the
[examples](https://github.com/haiiliin/abqcy/tree/main/examples) directory.

```{note}
In order to not mess up with the Cython declarations, you can add a companion `.pxd` file with the same name as your
Cython `.py` or `.pyx` file, and put the Cython declarations in it. See the
[examples](https://github.com/haiiliin/abqcy/tree/main/examples) for examples.
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
