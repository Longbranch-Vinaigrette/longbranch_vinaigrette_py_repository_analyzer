from .nodejs import NodeJS
from .python import Python


class RepositoryInformation:
    def __init__(self, repository_path: str):
        """Repository information"""
        self.path = repository_path

    def get_app_type(self):
        """Detect app type and get it"""
        try:
            python_app = Python(self.path)
            return python_app
        except:
            # Not a python app
            pass

        try:
            nodejs_app = NodeJS(self.path)
            return nodejs_app
        except:
            pass
