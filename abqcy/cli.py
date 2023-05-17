from __future__ import annotations

import os
import re
from pathlib import Path

from abqpy.cli import abaqus


class AbqcyCLI:
    """The ``abqcy`` command-line interface."""

    def compile(self, script: str):
        """Compile a Cython script to an Abaqus user subroutine as an object file."""
        os.system(f"cython -a {script}")
        compiled = Path(script).with_suffix(".c")
        replaced = re.sub("__PYX_EXTERN_C void ", 'extern "C" void ', compiled.read_text())
        compiled.write_text(replaced)
        abaqus.abaqus("make", library=str(compiled))
