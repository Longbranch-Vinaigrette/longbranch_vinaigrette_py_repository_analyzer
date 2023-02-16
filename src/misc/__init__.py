import os
import subprocess

from .. import cli_color_messages_python as ccm
from ..gitconfig import Gitconfig


def setup_submodules(app_path: str):
    """Setup/Install/Update submodules"""
    # Because I like submodules a lot :D
    # Use submodule py_gitconfig to extract data
    gitmodules_path = f"{app_path}{os.path.sep}.gitmodules"
    if os.path.exists(gitmodules_path):
        config = Gitconfig(gitmodules_path)
        gitconfig = config.loads()
    else:
        # The app/repository doesn't have submodules
        return

    # Get submodules paths
    for key in list(gitconfig.keys()):
        # This might not work on windows
        relative_path = f"{gitconfig[key]['path']}"
        submodule_path = f"{app_path}{os.path.sep}{relative_path}"
        is_empty = not os.listdir(submodule_path)

        if is_empty:
            # Install submodules and return
            ccm.print_ok_cyan(f"There's a submodule missing, installing every submodule "
                  f"in existence...")
            subprocess.run(["/bin/bash",
                            "-c",
                            # Cd our way in
                            f"cd {app_path};"
                            "git submodule update --remote --init --recursive --merge;"])
            ccm.print_ok_green("Submodules updated.")
            return
