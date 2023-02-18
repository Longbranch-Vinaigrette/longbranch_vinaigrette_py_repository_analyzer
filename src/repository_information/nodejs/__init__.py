import json
import os
import subprocess

from ... import cli_color_messages_python as ccm

from ... import misc


class NodeJS:
    def __init__(self, app_path: str):
        """Python app"""
        self.path = app_path
        self.framework = "Node.js"

        if not self.is_nodejs_app():
            raise Exception("Not a NodeJS app.")

    """
            Information
    """
    def has_indexjs(self):
        """Has index.js"""
        if os.path.exists(f"{self.path}{os.path.sep}index.js"):
            return True
        return False

    def is_nextjs_app(self):
        """Is next.js app"""
        if os.path.exists(f"{self.path}{os.path.sep}next.config.js"):
            return True
        return False

    def is_nodejs_app(self):
        """Check if it's a Node.js"""
        if self.has_indexjs():
            return True
        elif self.is_nextjs_app():
            return True
        else:
            return False

    def possible_start_commands(self):
        """Possible start commands

        Remember to use 'starts_with' and don't do this:
        CMD == python"""
        # Node.js with nvm
        # It could be any version, but at the end of the
        # day it's still a nodejs app, so with the previous path given
        # it's enough for precise identification
        nvm_path = f"{os.path.expanduser('~')}{os.path.sep}" \
            f".nvm{os.path.sep}" \
            f"versions{os.path.sep}" \
            f"node{os.path.sep}"

        return ["node", nvm_path]

    def exclude_start_commands(self):
        """Apps that started with these commands should be excluded"""
        # Why npm?
        # Because in the case it's a Next.js app, when you kill the npm
        # command that ran the app, it will not kill the actual app, just
        # the process on the console that tracks the app information.
        npm_command = "npm"

        # This command doesn't end the app process either
        bash_command = "bash"
        return [npm_command, bash_command]

    def possible_arguments(self):
        """Possible arguments given when the app started"""
        return [# For next.js apps
                f"{self.path}{os.path.sep}"
                f"node_modules{os.path.sep}"
                f".bin{os.path.sep}"
                f"next"]

    def app_language(self):
        """Get app language"""
        return "Javascript"

    def get_app_framework(self):
        """Get app framework"""
        if os.path.exists(f"{self.path}{os.path.sep}next.config.js"):
            self.framework = "Node.js/Next.js"
        else:
            package_json_path = f"{self.apth}{os.path.sep}package.json"
            if os.path.exists(package_json_path):
                # Get data
                with open(package_json_path) as f:
                    data = json.load(f)

                    # Now let's check what frameworks the app is using, by
                    # checking its dependencies
                    deps: dict = data["dependencies"]
                    frameworks = ["express"]
                    for dep in list(deps.keys()):
                        if dep in frameworks:
                            self.framework = f"Node.js/{dep}"
                            break

        return self.framework

    def get_nodejs_commands(self):
        """Get nodejs commands

        If it finds build it adds it
        And at last, after building, it adds the start command"""
        package_json_path = f"{self.path}{os.path.sep}package.json"
        cmds = ""
        if os.path.exists(package_json_path):
            # Fetch commands
            with open(package_json_path) as f:
                try:
                    data = json.load(f)

                    if "scripts" in data:
                        scripts = data['scripts']

                        # Only for Next.js apps
                        if self.is_nextjs_app():
                            if "build" in scripts:
                                cmds += f"npm run build;"
                                ccm.print_ok_blue("Found build script")
                            else:
                                ccm.print_warning(
                                    "The app doesn't have a build script "
                                    "but it was detected that the app may need it "
                                    "to start."
                                )
                                print("App types that may require to be "
                                      "built first: Next.js, React.js")

                        if "start" in scripts:
                            cmds += f"npm run start;"
                            ccm.print_ok_blue("Found start script")
                        else:
                            ccm.print_warning(
                                "No start script found running in simple "
                                "mode 'node index.js'"
                            )
                            # "If start doesn't exist, just start it normally"
                            # - Sigma grindset rule #3492929525235234243245235
                            cmds += f"node index.js"
                    else:
                        ccm.print_warning(
                            "Scripts field doesn't exist in package.json"
                        )
                        # Start normally
                        cmds += f"node index.js"
                except Exception as ex:
                    # Start normally
                    ccm.print_warning(
                        "Couldn't load data from package.json"
                    )
                    cmds += f"node index.js"
        else:
            ccm.print_warning(
                "No package.json found running in simple mode with the command "
                "'node index.js'"
            )
            cmds += f"node index.js"

        return cmds

    def get_app_run_command(self):
        """Get app run command

        First it checks if the app has a main.py file

        Then it checks if the app has a package.json
        If it doesn't find any commands in it, it will just run
        'node index.js'
        """
        # Node.js
        package_json_path = f"{self.path}{os.path.sep}package.json"

        cmds = ""

        # It's a python app
        if os.path.exists(package_json_path):
            # Commands
            cmds = "npm install;"
            cmds += self.get_nodejs_commands()

        return cmds

    """
            Operations
    """
    def start_app(self):
        """Installs dependencies, builds the app, and starts it

        Note that it doesn't update/install submodules
        """
        try:
            misc.setup_submodules(self.path)

            # Get app run command
            run_cmd = self.get_app_run_command()

            if not run_cmd:
                # Error
                return print_error("Couldn't find a way to run the Node.js app.")

            cmd = f"cd {self.path}; {run_cmd}"

            # Run app
            process = subprocess.run(["/bin/bash",
                                   "-c",
                                   cmd])

            if process.stdout:
                ccm.print_ok_green("Output:")
                print(process.stdout)

            if process.stderr:
                ccm.print_error("Error(Exit code != 0): " + process.stderr)

            return process
        except Exception as ex:
            return ccm.print_error(f"Error when trying to run the app, error: "
                                   f"{str(ex)}")
