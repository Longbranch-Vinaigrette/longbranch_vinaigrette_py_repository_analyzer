import subprocess

from .repository_process_manager import RepositoriesProcessManager


class RepositoriesProcesses:
    def __init__(self, repositories_path: list, debug: bool = False):
        rep_mng = RepositoriesProcessManager(repositories_path, debug=debug)
        self.apps_running = rep_mng.get_running_apps()

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
        return self.apps_running

    def get_app_running_by_cwd(self, path: str):
        """It's 99% likely that the app is the correct one, unless you
        have two apps on the same location that run with the same command,
        well then just search again or something."""
        return self.apps_running[path]
