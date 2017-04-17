#!/usr/bin/python3

import sys
import subprocess
import datetime

from debian.create import create_debian_packages_and_scripts
from brew.create import create_homebrew_packages_and_scripts


def execute_scripts(scripts, target_location):
    """ Executes all generated scripts.
    """
   #print(scripts)
   #api_key = input(
   #        "If you want the packages to be uploaded to BinTray "
   #        "please enter your API key: ").strip()
    def run(script_name, path):
        print('bash', script_name, target_location)
        process = subprocess.Popen(
                ('bash', script_name, target_location),
                cwd=path)
        if process.wait() != 0:
            raise Exception(script_name)
   #if api_key:
    for script, path in scripts:
        run(script, path)


def main(argv):
    """ Script entry point.
    """
    package_revision = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))

    if argv[1] == 'debian':
        scripts = create_debian_packages_and_scripts(
                package_revision,
                only_snapshots=False)
    elif argv[1] == 'homebrew':
        scripts = create_homebrew_packages_and_scripts(
                package_revision)
    else:
        raise Exception('Unknown platform: {}'.format(argv[1]))

    target_location = argv[2]

    execute_scripts(scripts, target_location)


if __name__ == '__main__':
    main(sys.argv)
