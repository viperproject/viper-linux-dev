from brew import config
from brew import packages
from scripts.create import (
    create_repository_setup_script,
    PackageManager,
    )
from scripts.uploader import (
    create_upload_script,
    )


class HomebrewPackageManager(PackageManager):

    def __init__(self, package_revision):
        super(HomebrewPackageManager, self).__init__()
        self.common_parameters = {
                'package_revision': package_revision,
                }

    def create_jar_package(self, **kwargs):
        kwargs.update(self.common_parameters)
        return packages.JARHomebrewPackage(**kwargs)

    def create_z3_package(self, **kwargs):
        kwargs.update(self.common_parameters)
        return packages.Z3HomebrewPackage(**kwargs)

    def create_boogie_package(self, **kwargs):
        kwargs.update(self.common_parameters)
        return packages.BoogieHomebrewPackage(**kwargs)

    def create_viper_package(self, **kwargs):
        kwargs.update(self.common_parameters)
        return packages.ViperHomebrewPackage(**kwargs)

    def get_uploadable_packages(self):
        packages = self.jar_packages[:]
        packages.append(self.viper_package)
        return packages


def create_homebrew_repository_setup_script(packages):
    """ Creates a shell script that creates packages on BinTray
    repository.
    """
    create_repository_setup_script(
            packages,
            config.REPOSITORY_SETUP_SCRIPT,
            config.REPOSITORY_NAME,
            )
    return config.REPOSITORY_SETUP_SCRIPT


def create_homebrew_upload_script(packages):
    """ Creates a shell script that uploads JAR and tar.gz files to
    BinTray repository.
    """
    calls = [
        (
          ('-X', 'PUT'),
          ('-T', package.file_path),
          ("$URL", (
            '{package_name}/{version}/{file_name};'
            'publish=1;override=1').format(
                package_name=package.package.long_name,
                version=package.full_version,
                file_name=package.file_name,
                )
            )
          )
        for package in packages
        ]
    create_upload_script(
        config.UPLOAD_SCRIPT,
        config.REPOSITORY_NAME,
        calls)
    return config.UPLOAD_SCRIPT


def create_homebrew_packages_and_scripts(package_revision):
    """ Creates homebrew package structures and build and upload scripts.
    """

    manager = HomebrewPackageManager(package_revision)
    manager.create_package_list()
    manager.create_package_structures()
    packages = manager.get_uploadable_packages()
    scripts = [
        create_homebrew_repository_setup_script(packages),
        create_homebrew_upload_script(packages),
        ]
    return [
        (script, config.BUILD_DIR)
        for script in scripts
        ]
