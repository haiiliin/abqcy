# Tutorial

This page is a tutorial for the `abqcy` project.
It will guide you through the whole workflow of using `abqcy` to write an Abaqus user subroutine,
create the model, extract the outout data, and visualize the results in a single command.

```{image} /tutorials/workflows.*
:align: center
:width: 100%
```

## 1. Write the user subroutine

The Abaqus user subroutine can be written in a Cython file.
The subroutine is very similar to a Abaqus C/C++ subroutine, except that it is written in Cython syntax.
Check {doc}`examples` for some simple examples.

## 2. Create the model as an Abaqus input file

You can use the Python script to create an Abaqus model, check
[abqpy tutorials](https://abqpy.readthedocs.io/en/stable/tutorials.html) for a simple example.
Noted that in the Python script, you should save the model into an Abaqus input file (`.inp`), 
so that the `abqcy` can read the model from the input file. For example:

```python
# Job
job = mdb.Job(name="element", model="Model-1")
job.writeInput()
```

If you are not familiar with Abaqus Python scripting, you can also use the Abaqus/CAE GUI to create an input file directly.

## 3. Write Python script to extract the output data from the Abaqus output database

You can use the Python script to extract the output data from the Abaqus output database (`.odb`).
You can also find a simple example in the [abqpy tutorials](https://abqpy.readthedocs.io/en/stable/tutorials.html#extract-output-data).
Typically, this Python script will extract the output data from the Abaqus output database and save it into a data file.

## 4. Visualize the results

Data extracted from the Abaqus output database can be visualized using another Python script.
For example, you can use the [matplotlib](https://matplotlib.org/) library to plot the data.

## 5. Run the `abqcy` command

After all the above steps are completed, you can run the `abqcy run` to finish the whole workflow:

```shell
abqcy run --model=<script-or-inp> --user=<subroutine> --post=<script> --visualiation=<script>
```

In chronological order, the `abqcy run` command will:

- Generate an Abaqus input file from the Python script, if the `--model` option is a Python script.
- Compile the user subroutine to an object file (`.obj`), if the `--user` option is a Cython file.
- Run the Abaqus analysis with the `abaqus input=<inp> user=<obj>` command.
- Run the post-processing Python script with the `abaqus cae noGUI=<script>` command.
- Run the visualization Python script with the `python <script>` command, using the current Python interpreter
  (the Python interpreter where `abqcy` is installed) to visualize the results.

## Example

The following is an example of scripts required by the `abqcy run` command:

````{tab} Subroutine
```{literalinclude} /tutorials/elastic.pyx
:language: cython
:linenos:
```
````

````{tab} Model Script
```{literalinclude} /tutorials/element.py
:language: python3
:linenos:
```
````

````{tab} Post-Process
```{literalinclude} /tutorials/element-output.py
:language: python3
:linenos:
```
````

````{tab} Visualization
```{literalinclude} /tutorials/element-visualization.py
:language: python3
:linenos:
```
````

````{tab} Execution
```{literalinclude} /tutorials/run.bat
:language: shell
:linenos:
```
````

```{note}
You can check all the files in the [`docs/tutorials`](https://github.com/haiiliin/abqcy/tree/main/docs/tutorials)
folder of the [`abqcy`](https://github.com/haiiliin/abqcy) repository.
```
