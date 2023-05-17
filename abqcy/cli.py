from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

from abqpy.cli import abaqus
from Cython.Build import cythonize


class AbqcyCLI:
    """The ``abqcy`` command-line interface."""

    def compile(
        self,
        script: str,
        *,
        exclude: list = None,
        nthreads: int = 0,
        aliases: dict = None,
        quiet: bool = False,
        force: bool = False,
        language: str = None,
        exclude_failures: bool = False,
        annotate: bool = True,
        **kwargs,
    ):
        """Compile a Cython script to an Abaqus user subroutine as an object file.

        Parameters
        ----------
        script : str
            The path to the Cython script to compile.
        exclude : list, optional
            When passing glob patterns as ``script``, you can exclude certain
            module names explicitly by passing them into the ``exclude`` option.
        nthreads : int, optional
            The number of concurrent builds for parallel compilation
            (requires the ``multiprocessing`` module).
        aliases : dict, optional
            If you want to use compiler directives like ``# distutils: ...`` but
            can only know at compile time (when running the ``setup.py``) which values
            to use, you can use aliases and pass a dictionary mapping those aliases
            to Python strings when calling :func:`cythonize`. As an example, say you
            want to use the compiler
            directive ``# distutils: include_dirs = ../static_libs/include/``
            but this path isn't always fixed and you want to find it when running
            the ``setup.py``. You can then do ``# distutils: include_dirs = MY_HEADERS``,
            find the value of ``MY_HEADERS`` in the ``setup.py``, put it in a python
            variable called ``foo`` as a string, and then call
            ``cythonize(..., aliases={'MY_HEADERS': foo})``.
        quiet : bool, optional
            If True, Cython won't print error, warning, or status messages during the
            compilation.
        force : bool, optional
            Forces the recompilation of the Cython modules, even if the timestamps
            don't indicate that a recompilation is necessary.
        language : str, optional
            To globally enable C++ mode, you can pass ``language='c++'``. Otherwise, this
            will be determined at a per-file level based on compiler directives.  This
            affects only modules found based on file names.  Extension instances passed
            into :func:`cythonize` will not be changed. It is recommended to rather
            use the compiler directive ``# distutils: language = c++`` than this option.
        exclude_failures : bool, optional
            For a broad 'try to compile' mode that ignores compilation
            failures and simply excludes the failed extensions,
            pass ``exclude_failures=True``. Note that this only
            really makes sense for compiling ``.py`` files which can also
            be used without compilation.
        annotate : bool, optional
            Whether to generate an HTML file with annotations, by default True.
        kwargs
            Additional keyword arguments to pass to the ``cythonize`` function.
        """
        cythonize(script, exclude=exclude, nthreads=nthreads, aliases=aliases, quiet=quiet, force=force,
                  language=language, exclude_failures=exclude_failures, annotate=annotate, **kwargs)  # fmt: skip
        compiled = Path(script).with_suffix(".c")
        replaced = re.sub("__PYX_EXTERN_C void ", 'extern "C" void ', compiled.read_text())
        compiled.write_text(replaced)
        abaqus.abaqus("make", library=str(compiled))

    def run(
        self,
        input: str,
        user: str,
        *,
        job: str = None,
        output: str = None,
        script: str = None,
        **kwargs,
    ):
        """Run Abaqus jobs.

        Parameters
        ----------
        input : str
            The path to the input file.
        user : str
            The name of the user subroutine.
        job : str, optional
            The name of the job, by default the current directory name.
        output : str, optional
            The path to the output directory, by default the current directory.
        script : str, optional
            The Python script to run after finishing the job to post-process the results.
        kwargs
            Additional keyword arguments to pass to the ``abaqus`` command to make the object file.
        """
        # Prepare the working directory
        output = Path(output or ".").resolve()
        job = job or Path(input).stem
        if not output.exists():
            output.mkdir(parents=True)
        if not (output / Path(input).name).exists():
            shutil.copy(input, output)
        if not (output / Path(user).name).exists():
            shutil.copy(user, output)
        if script and not (output / Path(script).name).exists():
            shutil.copy(script, output)
        os.chdir(output)

        # Compile the user subroutine if it is a Cython/Pure Python script
        if user.endswith((".pyx", ".py")):
            self.compile(Path(user).name)
            compiled = False
            for file in output.glob(f"{Path(user).stem}-*.obj"):
                user = file
                compiled = True
                break
            assert compiled, f"Failed to compile {user} to an object file."

        # Run the job
        inp = Path(input).stem
        user = Path(user).stem
        abaqus.abaqus("", job=job, input=inp, user=user, interactive=True, **kwargs)

        # Run the post-processing script
        if script:
            script = Path(script).name
            abaqus.cae(script, gui=False)
