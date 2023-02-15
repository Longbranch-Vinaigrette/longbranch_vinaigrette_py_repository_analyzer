import os


class NodeJS:
    def __init__(self, app_path: str):
        """Python app"""
        self.path = app_path

        if not self.is_nodejs_app():
            raise Exception("Not a NodeJS app.")

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

    def setup_and_run(self):
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

                        if "build" in scripts:
                            cmds += f"npm run build;"
                            print(f"{clr.OKBLUE}Found build script{clr.ENDC}")
                        else:
                            print(f"{clr.OKBLUE}The app doesn't uses a build script "
                                  f"{clr.ENDC}")

                        if "start" in scripts:
                            cmds += f"npm run start;"
                        else:
                            print(f"{clr.WARNING} Warning: No start script found "
                                  f"running in simple mode 'node index.js'{clr.ENDC}")
                            # "If start doesn't exist, just start it normally"
                            # - Sigma grindset rule #3492929525235234243245235
                            cmds += f"node index.js"
                    else:
                        print(f"{clr.WARNING}Warning: Scripts field doesn't exist "
                              f"in package.json{clr.ENDC}")
                        # Start normally
                        cmds += f"node index.js"
                except:
                    # Start normally
                    print(f"{clr.WARNING}Warning: Couldn't load data from "
                          f"package.json{clr.ENDC}")
                    cmds += f"node index.js"
        return cmds

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
