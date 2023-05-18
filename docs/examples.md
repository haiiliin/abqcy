# Examples

Below are some examples of how to use the library.
To compile the examples into an object file (`.obj`) that can be used by Abaqus, you can run the following command:
```shell
abqcy compile <path-to-your-subroutine>
```

## Example 1: Elastic `umat` subroutine

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
````
