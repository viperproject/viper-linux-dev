#!/usr/bin/python3

import os
import shutil
import datetime
import json
import subprocess
from glob import glob
from os import path

from scripts.packages import PACKAGES


ROOT_DIR = '/home/developer/source'
JARS_DIR = path.join(ROOT_DIR, 'chalice2silver/target/universal/stage/lib')
JARS = path.join(JARS_DIR, '*.jar')
BUILD_DIR = path.join(ROOT_DIR, 'workspace', 'package')
BUILD_SCRIPT = os.path.join(BUILD_DIR, 'build')
REPOSITORY_SETUP_SCRIPT = os.path.join(BUILD_DIR, 'repository_setup')
UPLOAD_SCRIPT = os.path.join(BUILD_DIR, 'upload')
PACKAGE_REVISION = 1
#MAINTAINER = 'Viper Team <viper@inf.ethz.ch>'
MAINTAINER = 'Vytautas Astrauskas <vastrauskas@gmail.com>'
ARCHITECTURE = 'amd64'
DISTRIBUTION_CODENAME = 'trusty'


class DebianPackage:
    """ A Debian package.
    """

    def __init__(self,
            jar_path,
            package,
            package_revision,
            architecture,
            distribution_codename,
            maintainer):

        self.jar_path = jar_path
        self.package = package
        self.package_revision = package_revision
        self.architecture = architecture
        self.distribution_codename = distribution_codename
        self.maintainer = maintainer

        # Configuration.
        self.full_version = "{0}-{1}".format(
                package.version,
                package_revision,
                )
        self.package_name = 'viper-{0}'.format(
                package.long_name.replace('_', '-'))
        self.package_full_name = 'viper-{0}_{1}'.format(
                package.long_name,
                self.full_version,
                )
        self.package_dir = path.join(BUILD_DIR, self.package_full_name)
        self.jar_dir = path.join(self.package_dir, 'usr', 'lib', 'viper')
        self.meta_dir = path.join(self.package_dir, 'DEBIAN')
        self.deb_path = path.join(BUILD_DIR, self.package_full_name + ".deb")
        self.deb_name = path.basename(self.deb_path)

    def create_package_structure(self):
        """ Creates a folder from which a DEB file can be created.
        """
        self._create_directories()
        self._copy_files()
        self._create_meta_data()

    def _create_directories(self):
        os.makedirs(self.package_dir, exist_ok=True)
        os.makedirs(self.jar_dir, exist_ok=True)
        os.makedirs(self.meta_dir, exist_ok=True)

    def _copy_files(self):
        # Copy jar.
        shutil.copy(self.jar_path, self.jar_dir)

    def _create_meta_data(self):
        with open(path.join(self.meta_dir, 'control'), 'w') as fp:
            fp.write("""\
Package: {name}
Version: {version}
Section: java
Priority: optional
Architecture: {architecture}
Maintainer: {maintainer}
Description: {description_short}
""".format(
                maintainer=self.maintainer,
                name=self.package_name,
                version=self.package.version,
                description_short=self.package.full_name,
                architecture=self.architecture,
                ))


def create_build_script(debian_packages):
    """ Creates a shell script that builds DEB packages.
    """
    with open(BUILD_SCRIPT, 'w') as fp:
        fp.write('#!/bin/bash\n')
        for package in debian_packages:
            fp.write('dpkg-deb --build "{0}"\n'.format(
                package.package_full_name
                ))


def create_repository_setup_script(debian_packages):
    """ Creates a shell script that creates packages on BinTray
    repository.
    """
    with open(REPOSITORY_SETUP_SCRIPT, 'w') as fp:
        fp.write('#!/bin/bash\n')
        fp.write('set -x\n')
        fp.write('set -v\n')
        fp.write('USER=vakaras\n')
        fp.write('API_KEY=$1\n')
        fp.write('URL="https://api.bintray.com/packages/$USER/deb"\n')
        for package in debian_packages:
            if package.package.omit:
                continue
            fp.write(r'''
curl -X POST \
    "-u$USER:$API_KEY" \
     -H "Content-Type: application/json" \
     -d '{0}' \
     "$URL"
            '''.format(json.dumps({
                'name': package.package.long_name,
                'desc': (
                    'A Debian package automatically generated '
                    'from JAR “{0}” by using '
                    'https://bitbucket.org/viperproject/'
                    'viper-linux-dev/src/tip/packaging/debian/create.py '
                    'script.').format(package.package.full_name),
                'licenses': [
                    license.short_name
                    for license in package.package.licenses
                    ],
                'vcs_url': package.package.vcs_url,
                })))


def create_upload_script(debian_packages):
    """ Creates a shell script that uploads DEB files to BinTray
    repository.
    """
    with open(UPLOAD_SCRIPT, 'w') as fp:
        fp.write('#!/bin/bash\n')
        fp.write('set -x\n')
        fp.write('set -v\n')
        fp.write('USER=vakaras\n')
        fp.write('API_KEY=$1\n')
        fp.write('URL="https://api.bintray.com/content/$USER/deb"\n')
        for package in debian_packages:
            if package.package.omit:
                continue
            fp.write(r'''
curl -X PUT \
     -T "{deb_path}" \
    "-u$USER:$API_KEY" \
    "$URL/{package_name}/{version}/pool/main/m/{package_name}/{deb_name};deb_distribution={distribution};deb_component=main;deb_architecture={architecture};publish=1;override=1"
            '''.format(
                deb_path=package.deb_path,
                package_name=package.package.long_name,
                version=package.full_version,
                deb_name=package.deb_name,
                distribution=package.distribution_codename,
                architecture=package.architecture,
                ))


def create_package_structures(debian_packages):
    """ Creates folders from which DEB files can be created.
    """
    for debian_package in debian_packages:
        debian_package.create_package_structure()


def create_package_list():
    """ Creates a list of packages to be packaged.
    """
    debian_packages = []
    for jar_path in glob(JARS):
        file_name = path.basename(jar_path)
        for package in PACKAGES:
            if package.check(file_name):
                if not package.omit:
                    debian_package = DebianPackage(
                            jar_path=jar_path,
                            package=package,
                            package_revision=PACKAGE_REVISION,
                            architecture=ARCHITECTURE,
                            distribution_codename=DISTRIBUTION_CODENAME,
                            maintainer=MAINTAINER)
                    debian_packages.append(debian_package)
                break
        else:
            raise Exception('Could not find package information.')
    return debian_packages


def execute_scripts():
    """ Executes all generated scripts.
    """
    api_key = input(
            "If you want the packages to be uploaded to BinTray "
            "please enter your API key: ").strip()
    if api_key:
        print('bash', BUILD_SCRIPT, api_key)
        print('bash', REPOSITORY_SETUP_SCRIPT, api_key)
        print('bash', UPLOAD_SCRIPT, api_key)
        #subprocess.check_call('bash', BUILD_SCRIPT, api_key)
        #subprocess.check_call('bash', REPOSITORY_SETUP_SCRIPT, api_key)
        #subprocess.check_call('bash', UPLOAD_SCRIPT, api_key)


def main():
    """ Script entry point.
    """
    debian_packages = create_package_list()
    create_package_structures(debian_packages)
    create_build_script(debian_packages)
    create_repository_setup_script(debian_packages)
    create_upload_script(debian_packages)
    execute_scripts()


if __name__ == '__main__':
    main()
