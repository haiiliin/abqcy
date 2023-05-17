from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

from abqpy.cli import abaqus
from Cython.Build import cythonize


class AbqcyCLI:
    """The ``abqcy`` command-line interface."""

    def compile(self, script: str, *, annotate: bool = True, **kwargs):
        """Compile a Cython script to an Abaqus user subroutine as an object file.

        Parameters
        ----------
        script : str
            The path to the Cython script to compile.
        annotate : bool, optional
            Whether to generate an HTML file with annotations, by default True.
        **kwargs
            Additional keyword arguments to pass to the ``cythonize`` command.
        """
        cythonize(script, annotate=annotate, **kwargs)
        compiled = Path(script).with_suffix(".c")
        replaced = re.sub("__PYX_EXTERN_C void ", 'extern "C" void ', compiled.read_text())
        compiled.write_text(replaced)
        abaqus.abaqus("make", library=str(compiled))

    def run(self, input: str, user: str, job: str = None, output: str = None, script: str = None, **kwargs):
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
        **kwargs
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
