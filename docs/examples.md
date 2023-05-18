# Examples

Below are some examples of how to use the library.
To compile the examples into an object file (`.obj`) that can be used by Abaqus, you can run the following command:
```shell
abqcy compile <path-to-your-subroutine>
```

```{note}
It shoule be noted that temporary variables do not required to be typed in Cython excepted for integers.
In the following examples, the `cython.infer_types` directive is used to infer types of untyped variables in function
bodies including integers. This directive does a work similar to the `auto` keyword in C++ for the readers who are
familiar with this language feature. It can be of great help to cut down on the need to type everything,
but it also can lead to surprises.

See [Determining where to add types](https://cython.readthedocs.io/en/stable/src/quickstart/cythonize.html#determining-where-to-add-types)
for more information.
```

## Example: Elastic `umat` subroutine

This example shows how to write an Abaqus elastic `umat` subroutine in Cython.

````{tab} Cython (elastic.pyx)
```{literalinclude} ../examples/elastic.pyx
:language: cython
:linenos:
```
````

````{tab} Pure Python (elastic.py)
```{literalinclude} ../examples/elastic.py
:language: python3
:linenos:
```
```{note}
You will need to add the Cython header file (`.pxd`) along with the Python file (`.py`) in order to use the Cython
declarations.
```
````

````{tab} Cython Header (elastic.pxd)
```{literalinclude} ../examples/elastic.pxd
:language: cython
:linenos:
```
```{note}
This file is required to use the Cython declarations in the Python file (`.py`).
```
````
