#!/usr/bin/python3

import subprocess

from debian.create import create_debian_packages_and_scripts


def execute_scripts(scripts):
    """ Executes all generated scripts.
    """
    api_key = input(
            "If you want the packages to be uploaded to BinTray "
            "please enter your API key: ").strip()
    def run(script_name, path):
        print('bash', script_name, api_key)
        process = subprocess.Popen(
                ('bash', script_name, api_key),
                cwd=path)
        if process.wait() != 0:
            raise Exception(script_name)
    if api_key:
        for script, path in scripts:
            run(script, path)


def main():
    """ Script entry point.
    """
    package_revision = int(input('Revision number: '))

    scripts = create_debian_packages_and_scripts(package_revision)
    execute_scripts(scripts)


if __name__ == '__main__':
    main()
