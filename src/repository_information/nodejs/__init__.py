class NodeJS:
    def get_app_build_command(self):
        pass

    def get_app_start_command(self):
        pass

    def get_app_test_command(self):
        pass

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
