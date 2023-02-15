import os
import pprint

import psutil

from ... import cli_color_messages_python as clr
from ...repository_information import RepositoryInformation


class RepositoriesProcessManager:
    def __init__(self, repositories_path: list, debug: bool = False):
        repositories: list = []

        for repo_path in repositories_path:
            repositories.append(
                {
                    "name": repo_path.split(os.path.sep)[-1],
                    "path": repo_path,
                }
            )
        self.repositories = repositories
        self.debug = debug

        self.update_possible_apps_commands()

        self.repositories_index = {}
        for index, repository in enumerate(repositories):
            self.repositories_index[repository["path"]] = index

        if self.debug:
            for repository in repositories:
                if repository["appLanguage"] == "Python":
                    print("\n")
                    clr.print_underline(f"{repository['name']}")
                    pprint.pprint(repository)

        if self.debug:
            print("\n")
        self.apps_running = self.find_running_apps()

    def get_repository_by_path(self, path: str):
        """Get repository indexed by path for the classic O(1) performance"""
        try:
            return self.repositories[self.repositories_index[path]]
        except:
            pass

    def update_possible_apps_commands(self):
        """Set possible apps commands on every repository of the repository
        list"""
        for repository in self.repositories:
            info = RepositoryInformation(repository["path"])
            app_type = info.get_app_type()

            if app_type:
                possible_commands = app_type.possible_start_commands()
                repository["possibleCommands"] = possible_commands

                possible_start_scripts = app_type.possible_start_scripts()
                repository["possibleStartScripts"] = possible_start_scripts

                repository["appLanguage"] = app_type.app_language()
            else:
                repository["possibleCommands"] = None
                repository["possibleStartScripts"] = None
                repository["appLanguage"] = None

    def find_starts_with(self, cmd: str, possible_cmds: list):
        """Find the cmd of a process starts with at least one
        of the possible commands"""
        for possible_cmd in possible_cmds:
            if cmd.startswith(possible_cmd):
                return True
        return False

    def find_running_apps(self):
        """Find the app, if not found returns None"""
        # Get every running process
        processes = []
        for proc in psutil.process_iter(["pid", "name", "cmdline", "cwd"]):
            pinfo: str = proc.info
            processes.append(pinfo)

        # Check which repositories/apps are running and which aren't
        # It's a dictionary that uses the path as a key, you know
        # so you can access it without looping around.
        apps_running: dict = {}
        for proc in processes:
            app_info = self.get_repository_by_path(
                proc["cwd"]
            )

            if app_info:
                try:
                    # The name of the app is the command
                    is_the_app = self.find_starts_with(
                        proc["name"],
                        app_info["possibleCommands"])
                    if is_the_app:
                        if self.debug:
                            clr.print_ok_green(f"App found: {proc['name']}")
                            pprint.pprint(proc)

                        apps_running[proc["cwd"]] = proc
                except Exception as ex:
                    # This error is kinda tricky, that's why I added so much info
                    print("Exception: ", ex)
                    clr.print_error("It's likely that the possible commands field "
                                    "doesn't exist, you must update it on the "
                                    "submodule longbranch_vinaigrette_py_repository"
                                    "_analyzer/src/repository_information and its "
                                    "respective class.")
                    clr.print_itallic("Without the app possible commands it would "
                                      "be really hard to identify the app, you "
                                      "just need to add possible values to "
                                      "start the app, like: python3.10, node, "
                                      "etc.")
                    clr.print_underline("Process information")
                    pprint.pprint(proc)
                    clr.print_underline("App information")
                    pprint.pprint(app_info)
        return apps_running

    def get_running_apps(self):
        """Get running apps"""
        return self.apps_running
