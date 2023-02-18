import os
import pprint

import psutil

from ... import cli_color_messages_python as clr
from ...repository_information import RepositoryInformation


class RepositoriesProcessManager:
    def __init__(self, repositories_path: list, debug: bool = False):
        repositories: list = []

        # Get name and path
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
                # Any of these could be missing
                try:
                    possible_commands = app_type.possible_start_commands()
                    repository["possibleCommands"] = possible_commands
                except:
                    repository["possibleCommands"] = None

                try:
                    possible_start_scripts = app_type.possible_start_scripts()
                    repository["possibleStartScripts"] = possible_start_scripts
                except:
                    repository["possibleStartScripts"] = None

                # Get app framework
                try:
                    framework = app_type.get_app_framework()
                    repository["framework"] = framework
                except:
                    repository["framework"] = "Unknown"

                # App language shouldn't be missing in any case
                repository["appLanguage"] = app_type.app_language()
            else:
                repository["possibleCommands"] = None
                repository["possibleStartScripts"] = None
                repository["appLanguage"] = None
                repository["framework"] = "Unknown"

    def find_starts_with(self,
                         cmd: str,
                         possible_cmds: list,
                         excludes: list = []):
        """Find the cmd of a process starts with at least one
        of the possible commands"""
        for possible_cmd in possible_cmds:

            if cmd.startswith(possible_cmd):
                return True
        return False

    def get_this_is_not_it(self, cmd: str, excludes: list = []):
        """Check if this is the app we're looking for or not

        This one discards any app that its start command starts with a
        command given in the 'excludes' list"""
        for exclude in excludes:
            if cmd.startswith(exclude):
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
                    # Process name is essential on process identification
                    try:
                        process_name = proc["name"]
                    except:
                        clr.print_error("You need to provide the field 'name' "
                                        "for every process, as this is the command "
                                        "that started the process, and is "
                                        "used to identify the app.")
                        continue

                    # Check if the command is excluded or not, if it's
                    # then this is not the command we are looking for
                    try:
                        this_is_not_it = self.get_this_is_not_it(
                            process_name,
                            app_info.exclude_start_commands()
                        )
                        # Although this process may have started the app,
                        # killing it wouldn't stop the app, like Next.js
                        # 'npm run dev'
                        if this_is_not_it:
                            continue
                    except:
                        # The language apps have no excluded commands, and
                        # that's ok.
                        pass

                    # Check if there are possible start commands
                    # if there aren't, we can't kill the app then.
                    try:
                        app_possible_commands = app_info["possibleCommands"]
                        if not app_possible_commands:
                            raise Exception("The app needs possible starting commands "
                                        "to be precisely identified")
                    except:
                        clr.print_error("The app needs possible starting commands "
                                        "to be precisely identified")
                        continue

                    try:
                        process_cwd = proc["cwd"]
                    except:
                        clr.print_error("The process cwd is very important to "
                                        "identify app there must have been a weird "
                                        "error if you didn't get it, check what "
                                        "information you retrieve from the "
                                        "processes.")
                        continue

                    # The name of the app is the command
                    is_the_app = self.find_starts_with(
                        process_name,
                        app_possible_commands)

                    if is_the_app:
                        if self.debug:
                            clr.print_ok_green(f"App found: {proc['name']}")
                            pprint.pprint(proc)

                        apps_running[process_cwd] = {
                            **proc,
                            "appInfo": app_info
                        }
                except Exception as ex:
                    clr.print_error("Unknown error: ")
                    print(f"{clr.clr.FAIL}Exception: ", ex, f"{clr.clr.ENDC}")
        return apps_running

    def get_running_apps(self):
        """Get running apps"""
        return self.apps_running
