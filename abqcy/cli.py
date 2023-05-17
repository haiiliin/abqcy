from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

from abqpy.cli import abaqus


class AbqcyCLI:
    """The ``abqcy`` command-line interface."""

    def compile(self, script: str):
        """Compile a Cython script to an Abaqus user subroutine as an object file.

        Parameters
        ----------
        script : str
            The path to the Cython script to compile.
        """
        os.system(f"cython -a {script}")
        compiled = Path(script).with_suffix(".c")
        replaced = re.sub("__PYX_EXTERN_C void ", 'extern "C" void ', compiled.read_text())
        compiled.write_text(replaced)
        abaqus.abaqus("make", library=str(compiled))

    def run(self, input: str, user: str, job: str = None, wd: str = None, script: str = None, **kwargs):
        """Run Abaqus jobs.

        Parameters
        ----------
        input : str
            The path to the input file.
        user : str
            The name of the user subroutine.
        job : str, optional
            The name of the job, by default the current directory name.
        wd : str, optional
            The working directory, by default the directory of the input file.
        script : str, optional
            The Python script to run after finishing the job to post-process the results.
        """
        # Prepare the working directory
        wd = Path(wd or ".").resolve()
        job = job or Path(input).stem
        if not wd.exists():
            wd.mkdir(parents=True)
        if not (wd / Path(input).name).exists():
            shutil.copy(input, wd)
        if not (wd / Path(user).name).exists():
            shutil.copy(user, wd)
        if script and not (wd / Path(script).name).exists():
            shutil.copy(script, wd)
        os.chdir(wd)

        # Compile the user subroutine if it is a Cython/Pure Python script
        if user.endswith((".pyx", ".py")):
            self.compile(Path(user).name)
            compiled = False
            for file in wd.glob(f"{Path(user).stem}-*.obj"):
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
