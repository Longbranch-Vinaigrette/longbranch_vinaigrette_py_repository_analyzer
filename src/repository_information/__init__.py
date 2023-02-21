from .. import cli_color_messages_python as ccm

from .nodejs import NodeJS
from .python import Python


class RepositoryInformation:
    app = None
    
    def __init__(self, repository_path: str):
        """Repository information"""
        self.path = repository_path

    def get_app_type(self):
        """Detect app type and get it"""
        try:
            python_app = Python(self.path)
            self.app = python_app
            return python_app
        except:
            # Not a python app
            pass

        try:
            nodejs_app = NodeJS(self.path)
            self.app = nodejs_app
            return nodejs_app
        except Exception as ex:
            pass

    def get_app_info(self):
        """Get app info
        
        returns
            dict: A dictionary containing app information.
        """
        if not self.app:
            self.get_app_type()
        
        app_info: dict = {}
        if self.app:
            # Any of these could be missing
            try:
                possible_commands = self.app.possible_start_commands()
                app_info["possibleCommands"] = possible_commands
            except:
                app_info["possibleCommands"] = None

            try:
                possible_start_scripts = self.app.possible_start_scripts()
                app_info["possibleStartScripts"] = possible_start_scripts
            except:
                app_info["possibleStartScripts"] = None

            # Get app framework
            try:
                framework = self.app.get_app_framework()
                app_info["framework"] = framework
            except:
                app_info["framework"] = "Unknown"

            # App language shouldn't be missing in any case
            app_info["appLanguage"] = self.app.app_language()
        else:
            app_info["possibleCommands"] = None
            app_info["possibleStartScripts"] = None
            app_info["appLanguage"] = None
            app_info["framework"] = "Unknown"
        return app_info
