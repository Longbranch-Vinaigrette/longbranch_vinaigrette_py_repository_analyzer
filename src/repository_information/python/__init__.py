import os
import subprocess

from ... import cli_color_messages_python as ccm
from ... import misc
from ...packages import Packages


class Python:
    def __init__(self, app_path: str, run_args: str = ""):
        """Python app"""
        self.path = app_path
        self.args = run_args

        if not self.is_python_app():
            raise Exception("Not a python app.")

    def uses_pipenv(self):
        """Check if the app uses pipenv"""
        if os.path.exists(f"{self.path}{os.path.sep}Pipfile"):
            return True
        return False

    def has_main_dot_py(self):
        """Check if the app has main.py"""
        if os.path.exists(f"{self.path}{os.path.sep}main.py"):
            return True
        return False

    def has_manage_dot_py(self):
        """Basically is a Django app"""
        if os.path.exists(f"{self.path}{os.path.sep}manage.py"):
            return True
        return False

    def possible_start_commands(self):
        """Possible start commands

        Remember to use 'starts_with' and don't do this:
        CMD == python"""
        return ["python", "/usr/bin/python"]

    def possible_start_scripts(self):
        """Get possible start scripts"""
        start_scripts: list = []
        if self.has_main_dot_py():
            start_scripts.append("main.py")

        if self.has_manage_dot_py():
            start_scripts.append("manage.py")
        return start_scripts

    def is_python_app(self):
        """Is python app"""
        if self.uses_pipenv():
            return True
        elif self.has_main_dot_py():
            return True
        elif self.has_manage_dot_py():
            return True

    def app_language(self):
        """Get app language"""
        return "Python"

    def get_app_run_command(self):
        """Get app run command"""
        cmds = ""

        # Check if it uses pipenv
        if os.path.exists(f"{self.path}{os.path.sep}Pipfile"):
            # If the user doesn't have pipenv but the file Pipfile exists
            # in the folder, we can install it.
            pkgs = Packages()
            result = pkgs.find("pipenv")

            if not result:
                # "If the package doesn't exist, just install it" - Sigma grindset rule 420
                subprocess.run(["pip3", "install", "pipenv"])

            return f"pipenv run python3 main.py {self.args};"
        else:
            # Normal python app
            return f"python3 main.py {self.args};"

    """
            Operations
    """
    def start_app(self):
        """Start the app"""
        misc.setup_submodules(self.path)
        cmds = self.get_app_run_command()
        print("Cmds: ", cmds, "\n")

        if cmds:
            subprocess.run(["/bin/bash",
                            "-c",
                            f"cd {self.path}; {cmds}"])
        else:
            ccm.print_error("Couldn't find a way to run the Python app.")
