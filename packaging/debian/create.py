from glob import glob
from os import path

from debian import config
from debian import packages
from scripts.create import (
    create_repository_setup_script,
    )
from scripts.packages import (
    PACKAGES,
    Z3_PACKAGE,
    BOOGIE_PACKAGE,
    VIPER_PACKAGE,
    )
from scripts.uploader import (
    create_upload_script,
    )


def create_package_list(package_revision):
    """ Creates a list of packages to be packaged.
    """
    debian_packages = []
    for jar_path in glob(config.JARS):
        file_name = path.basename(jar_path)
        for package in PACKAGES:
            if package.check(file_name):
                if not package.omit:
                    debian_package = packages.JARDebianPackage(
                            jar_path=jar_path,
                            package=package,
                            package_revision=package_revision,
                            architecture=config.ARCHITECTURE,
                            distribution_codename=config.DISTRIBUTION_CODENAME,
                            maintainer=config.MAINTAINER,
                            short_description=(
                                'A Debian package automatically generated '
                                'from JAR “{0}” by using '
                                'https://bitbucket.org/viperproject/'
                                'viper-linux-dev/src/tip/packaging/'
                                'debian/create.py script.'
                                ).format(package.full_name),
                            )
                    debian_packages.append(debian_package)
                break
        else:
            raise Exception('Could not find package information.')
    debian_packages.append(packages.Z3DebianPackage(
        package=Z3_PACKAGE,
        package_revision=package_revision,
        architecture=config.ARCHITECTURE,
        distribution_codename=config.DISTRIBUTION_CODENAME,
        maintainer=config.MAINTAINER,
        short_description=(
            'Z3 is a theorem prover from Microsoft Research. '
            'This package contains a Z3 version that was tested '
            'to work with Viper.'
            )
        ))
    debian_packages.append(packages.BoogieDebianPackage(
        package=BOOGIE_PACKAGE,
        package_revision=package_revision,
        architecture=config.ARCHITECTURE,
        distribution_codename=config.DISTRIBUTION_CODENAME,
        maintainer=config.MAINTAINER,
        short_description=(
            'Boogie is an itermediate verification language from '
            'Microsoft Research.'
            )
        ))
    debian_packages.append(packages.ViperDebianPackage(
        debian_packages,
        package=VIPER_PACKAGE,
        package_revision=package_revision,
        architecture=config.ARCHITECTURE,
        distribution_codename=config.DISTRIBUTION_CODENAME,
        maintainer=config.MAINTAINER,
        short_description=(
            'A meta-package for installing Viper '
            '(http://www.pm.inf.ethz.ch/research/viper.html).'
            ),
        ))
    return debian_packages


def create_package_structures(packages):
    """ Creates folders from which DEB files can be created.
    """
    for package in packages:
        package.create_package_structure()


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
            'deb'
            )
    return config.REPOSITORY_SETUP_SCRIPT


def create_debian_upload_script(packages):
    """ Creates a shell script that uploads DEB files to BinTray
    repository.
    """
    calls = [
        (
          ('-X', 'PUT'),
          ('-T', package.deb_path),
          ("$URL", (
            '$URL/{package_name}/{version}/pool/main/m/'
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
        if not package.package.omit
        ]
    create_upload_script(
        config.UPLOAD_SCRIPT,
        'deb',
        calls)
    return config.UPLOAD_SCRIPT


def create_debian_packages_and_scripts(package_revision):
    """ Creates debian package structures and build and upload scripts.
    """

    packages = create_package_list(package_revision)
    create_package_structures(packages)
    scripts = [
        create_build_script(packages),
        create_debian_repository_setup_script(packages),
        create_debian_upload_script(packages)
        ]
    return [
        (script, config.BUILD_DIR)
        for script in scripts
        ]
