from brew import config
from brew import packages
from scripts.create import PackageManager


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

def create_homebrew_packages_and_scripts(package_revision):
    """ Creates homebrew package structures and build and upload scripts.
    """

    manager = HomebrewPackageManager(package_revision)
    manager.create_package_list()
    manager.create_package_structures()
    packages = manager.packages
    scripts = [
        create_build_script(packages),
        create_debian_repository_setup_script(packages),
        create_debian_upload_script(packages)
        ]
    return [
        (script, config.BUILD_DIR)
        for script in scripts
        ]
