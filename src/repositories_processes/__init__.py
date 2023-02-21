import subprocess

from ..repository_information import RepositoryInformation
from .. import cli_color_messages_python as ccm

from .repository_process_manager import RepositoriesProcessManager


class RepositoriesProcesses:
    def __init__(self,
                 repositories_path: list,
                 debug: bool = False):
        """

        only_running Whether to get only running apps or not
        """
        self.rep_proc_manager = RepositoriesProcessManager(repositories_path, debug=debug)

    def start_by_cwd(self, cwd: str):
        """Start an app by cwd"""
        rep_inf = RepositoryInformation(cwd)
        app = rep_inf.get_app_type()

        try:
            # Start app installs dependencies, builds the app(if necessary)
            # and then starts it.
            app.start_app()
            ccm.print_ok_green("App started successfully")
        except Exception as ex:
            ccm.print_error("Couldn't find a way to start the app.")
            ccm.print_error(f"Exception: {str(ex)}")

    def kill_by_cwd(self, cwd: str):
        """Kill an app precisely by cwd

        I doubt there's a better way to kill a program unless you already
        know its pid, also this is O(1)

        Returns its pid in case the signal 15 didn't work"""
        app_pid = self.apps_running[cwd]["pid"]
        subprocess.run([
            "kill", "-s", "15", str(app_pid)
        ])
        return app_pid

    def get_running_apps(self):
        """Get running apps"""
        return self.rep_proc_manager.get_running_apps()

    def get_apps(self):
        """Get every app running or not"""
        return self.rep_proc_manager.get_apps()

    def get_app_running_by_cwd(self, path: str):
        """It's 99% likely that the app is the correct one, unless you
        have two apps on the same location that run with the same command,
        well then just search again or something."""
        return self.apps_running[path]
