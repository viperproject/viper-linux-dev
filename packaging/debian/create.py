from debian import config
from debian import packages
from scripts.create import (
    create_repository_setup_script,
    )
from scripts.create import PackageManager
from scripts.uploader import (
    create_upload_script,
    )


class DebianPackageManager(PackageManager):

    def __init__(self, package_revision):
        super(DebianPackageManager, self).__init__()
        self.common_parameters = {
                'package_revision': package_revision,
                'architecture': config.ARCHITECTURE,
                'distribution_codename': config.DISTRIBUTION_CODENAME,
                'maintainer': config.MAINTAINER,
                }

    def create_jar_package(self, **kwargs):
        kwargs.update(self.common_parameters)
        return packages.JARDebianPackage(**kwargs)

    def create_z3_package(self, **kwargs):
        kwargs.update(self.common_parameters)
        return packages.Z3DebianPackage(**kwargs)

    def create_boogie_package(self, **kwargs):
        kwargs.update(self.common_parameters)
        return packages.BoogieDebianPackage(**kwargs)

    def create_viper_package(self, **kwargs):
        kwargs.update(self.common_parameters)
        return packages.ViperDebianPackage(**kwargs)


def create_build_script(debian_packages):
    """ Creates a shell script that builds DEB packages.
    """
    with open(config.BUILD_SCRIPT, 'w') as fp:
        fp.write('#!/bin/bash\n')
        for package in debian_packages:
            fp.write('dpkg-deb --build "{0}"\n'.format(
                package.package_full_name
                ))
    return config.BUILD_SCRIPT


def create_debian_repository_setup_script(debian_packages):
    """ Creates a shell script that creates packages on BinTray
    repository.
    """
    create_repository_setup_script(
            debian_packages,
            config.REPOSITORY_SETUP_SCRIPT,
            config.REPOSITORY_NAME,
            )
    return config.REPOSITORY_SETUP_SCRIPT


def create_copy_script(packages):
    """ Creates a shell script that copies DEB files to the specified
    directory.
    """
    with open(config.COPY_SCRIPT, 'w') as fp:
        fp.write('#!/bin/bash\n')
        fp.write('set -x\n')
        fp.write('set -v\n')
        for package in packages:
            if not package.package.omit:
                fp.write('cp "{}" "$1"\n'.format(package.deb_path))
    return config.COPY_SCRIPT


def create_debian_upload_script(packages, only_snapshots):
    """ Creates a shell script that uploads DEB files to BinTray
    repository.
    """
    calls = [
        (
          ('-X', 'PUT'),
          ('-T', package.deb_path),
          ("$URL", (
            '{package_name}/{version}/pool/main/m/'
            '{package_name}/{deb_name};deb_distribution={distribution};'
            'deb_component=main;deb_architecture={architecture};'
            'publish=1;override=1').format(
                package_name=package.package.long_name,
                version=package.full_version,
                deb_name=package.deb_name,
                distribution=package.distribution_codename,
                architecture=package.architecture,
                )
            )
          )
        for package in packages
        if not package.package.omit and
           (package.package.is_snapshot or not only_snapshots)
        ]
    create_upload_script(
        config.UPLOAD_SCRIPT,
        config.REPOSITORY_NAME,
        calls)
    return config.UPLOAD_SCRIPT


def create_debian_packages_and_scripts(package_revision, only_snapshots):
    """ Creates debian package structures and build and upload scripts.
    """

    manager = DebianPackageManager(package_revision)
    manager.create_package_list()
    manager.create_package_structures()
    packages = manager.packages
    scripts = [
        create_build_script(packages),
        create_copy_script(packages),
       #create_debian_repository_setup_script(packages),
       #create_debian_upload_script(packages, only_snapshots)
        ]
    return [
        (script, config.BUILD_DIR)
        for script in scripts
        ]
