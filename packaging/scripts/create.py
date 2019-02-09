import json

from glob import glob
from os import path

from scripts import config
from scripts.packages import (
    PACKAGES,
    Z3_PACKAGE,
    BOOGIE_PACKAGE,
    VIPER_PACKAGE,
    )
from scripts.uploader import create_repository_setup_script as cr


class PackageManager:
    """ Creates a list of packages to be packaged.

    Implements method template design pattern.
    """

    def __init__(self):
        self.jar_packages = []
        self.binary_packages = []
        self.viper_package = None
        self.packages = []

    def get_jar_paths(self):
        return glob(config.JARS)

    def create_package_list(self):
        self.create_jar_package_list()
        self.create_binary_package_list()
        self.create_viper_package_wrapper()
        self.packages = self.jar_packages + self.binary_packages
        self.packages.append(self.viper_package)

    def detect_jar_version(self, file_name):
        version = file_name[:-4]
        version = version.replace('-SNAPSHOT', '')
        for part in reversed(version.split('-')):
            if part[0].isdigit():
                version = part
        return version

    def create_jar_package_list(self):
        for jar_path in self.get_jar_paths():
            file_name = path.basename(jar_path)
            for package_info in PACKAGES:
                if package_info.check(file_name):
                    if not package_info.omit:
                        jar_version = self.detect_jar_version(file_name)
                        package = self.create_jar_package(
                            jar_path=jar_path,
                            jar_version=jar_version,
                            package=package_info,
                            short_description=(
                              'A package automatically generated '
                              'from JAR “{0} # {1} # {2}” by using '
                              'https://bitbucket.org/viperproject/'
                              'viper-linux-dev/src/tip/packaging/'
                              'create.py script.'
                              ).format(
                                package_info.prefix,
                                package_info.name,
                                jar_version,
                                ),
                            )
                        self.jar_packages.append(package)
                    break
            else:
                raise Exception(
                    'Could not find package information. jar_path={}'.format(
                        jar_path))

    def create_binary_package_list(self):
        self.binary_packages.extend([
          self.create_z3_package_wrapper(),
          self.create_boogie_package_wrapper(),
          ])

    def create_z3_package_wrapper(self):
        return self.create_z3_package(
            package=Z3_PACKAGE,
            short_description=(
                'Z3 is a theorem prover from Microsoft Research. '
                'This package contains a Z3 version that was tested '
                'to work with Viper.'
                )
            )

    def create_boogie_package_wrapper(self):
        return self.create_boogie_package(
            package=BOOGIE_PACKAGE,
            short_description=(
                'Boogie is an itermediate verification language from '
                'Microsoft Research.'
                )
            )

    def create_viper_package_wrapper(self):
        self.viper_package = self.create_viper_package(
            jar_packages=self.jar_packages,
            binary_packages=self.binary_packages,
            package=VIPER_PACKAGE,
            short_description=(
                'A meta-package for installing Viper '
                '(http://www.pm.inf.ethz.ch/research/viper.html).'
                )
            )

    def create_package_structures(self):
        """ Creates folders from which DEB files can be created.
        """
        for package in self.packages:
            package.create_package_structure()


def create_repository_setup_script(
        packages,
        repository_setup_script,
        repository_name):
    """ Creates a shell script that creates packages on BinTray
    repository.
    """
    calls = [
        (
          ('-X', 'POST'),
          ('-H', 'Content-Type: application/json'),
          ('-d', json.dumps({
                'name': package.package.long_name,
                'desc': package.short_description,
                'licenses': [
                    license.short_name
                    for license in package.package.licenses
                    ],
                'vcs_url': package.package.vcs_url,
                }))
          )
        for package in packages
        if not package.package.omit
        ]
    cr(
        repository_setup_script,
        repository_name,
        calls)
