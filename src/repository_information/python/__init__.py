import os


class Python:
    def __init__(self, app_path: str):
        """Python app"""
        self.path = app_path

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
