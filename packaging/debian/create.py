#!/usr/bin/python3

import os
import shutil
import datetime
import json
import subprocess
from glob import glob
from os import path

from scripts.packages import (
        PACKAGES,
        Z3_PACKAGE,
        BOOGIE_PACKAGE,
        VIPER_PACKAGE,
        )


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

    This class implements method template design pattern.
    """

    def __init__(self,
            package,
            package_revision,
            architecture,
            distribution_codename,
            maintainer,
            short_description):

        self.package = package
        self.package_revision = package_revision
        self.architecture = architecture
        self.distribution_codename = distribution_codename
        self.maintainer = maintainer
        self.short_description = short_description
        self.section = None     # Expected to be set in subclasses.
        self.depends = None     # Expected to be set in subclasses.

        # Configuration.
        self.full_version = "{0}-{1}".format(
                package.version,
                package_revision,
                )
        self.package_dir = path.join(BUILD_DIR, self.package_full_name)
        self.meta_dir = path.join(self.package_dir, 'DEBIAN')
        self.deb_path = path.join(BUILD_DIR, self.package_full_name + ".deb")
        self.deb_name = path.basename(self.deb_path)

    @property
    def package_name(self):
        return 'viper-{0}'.format(self.package.long_name.replace('_', '-'))

    @property
    def package_full_name(self):
        return '{0}_{1}'.format(self.package_name, self.full_version)

    def create_package_structure(self):
        """ Creates a folder from which a DEB file can be created.
        """
        self._create_directories()
        self._copy_files()
        self._create_meta_data()

    def _copy_files(self):
        """ This is abtract method.
        """

    def _create_directories(self):
        """ This is abtract method.
        """

    def _create_meta_data(self):
        with open(path.join(self.meta_dir, 'control'), 'w') as fp:
            def write(field, value):
                fp.write('{0}: {1}\n'.format(field, value))
            write('Package', self.package_name)
            write('Version', self.full_version)
            write('Section', self.section)
            write('Priority', 'optional')
            write('Architecture', self.architecture)
            if self.depends:
                write('Depends', self.depends)
            write('Maintainer', self.maintainer)
            write('Description', self.short_description)


class JARDebianPackage(DebianPackage):
    """ A Debian package encapsulating JAR file.
    """

    def __init__(self, jar_path, *args, **kwargs):
        super(JARDebianPackage, self).__init__(*args, **kwargs)
        self.section = 'java'
        self.jar_path = jar_path
        self.jar_dir = path.join(self.package_dir, 'usr', 'lib', 'viper')
        self.depends = 'default-jre'

    def _create_directories(self):
        os.makedirs(self.package_dir, exist_ok=True)
        os.makedirs(self.jar_dir, exist_ok=True)
        os.makedirs(self.meta_dir, exist_ok=True)

    def _copy_files(self):
        # Copy jar.
        shutil.copy(self.jar_path, self.jar_dir)


class Z3DebianPackage(DebianPackage):
    """ A Debian package for Z3.
    """

    def __init__(self, *args, **kwargs):
        super(Z3DebianPackage, self).__init__(*args, **kwargs)
        self.section = 'base'
        self.bin_dir = path.join(self.package_dir, 'usr', 'bin')
        self.depends = 'libgomp1'

    def _create_directories(self):
        os.makedirs(self.package_dir, exist_ok=True)
        os.makedirs(self.bin_dir, exist_ok=True)
        os.makedirs(self.meta_dir, exist_ok=True)

    def _copy_files(self):
        # Copy binary.
        shutil.copy('/usr/bin/z3', path.join(self.bin_dir, 'viper-z3'))


class ViperDebianPackage(DebianPackage):
    """ A package that has a dependency on all other packages.

    Also it contains shell scripts for invocation.
    """

    def __init__(self, debian_packages, *args, **kwargs):
        super(ViperDebianPackage, self).__init__(*args, **kwargs)
        self.section = 'base'
        self.bin_dir = path.join(self.package_dir, 'usr', 'bin')
        dependencies = [
                package.package_name
                for package in debian_packages
                ]
        dependencies.append('nailgun')
        self.depends = ', '.join(dependencies)

    @property
    def package_name(self):
        return 'viper'

    def _create_directories(self):
        os.makedirs(self.package_dir, exist_ok=True)
        os.makedirs(self.bin_dir, exist_ok=True)
        os.makedirs(self.meta_dir, exist_ok=True)

    def _copy_files(self):
        configurations = [
                ('silicon', 'viper.silicon.SiliconRunner'),
                ('carbon', 'viper.carbon.Carbon'),
                ('chalice2silver', 'viper.chalice2sil.Program'),
                ]
        for script_name, cls in configurations:
            script_path = path.join(self.bin_dir, script_name)
            with open(script_path, 'w') as fp:
                fp.write('#!/bin/bash\n')
                fp.write('JARS=($(ls /usr/lib/viper/*.jar))\n')
                fp.write('CP=$(printf ":%s" "${JARS[@]}")\n')
                fp.write('CP=${CP:1}\n')
                fp.write('export Z3_EXE=/usr/bin/viper-z3\n')
                fp.write('export BOOGIE_EXE=/usr/bin/boogie\n')
                fp.write('java -Xss30M -cp "$CP" {0} $@\n'.format(cls))


class BoogieDebianPackage(DebianPackage):
    """ A Debian package for Boogie.
    """

    def __init__(self, *args, **kwargs):
        super(BoogieDebianPackage, self).__init__(*args, **kwargs)
        self.section = 'base'
        self.bin_dir = path.join(self.package_dir, 'usr', 'bin')
        self.lib_dir = path.join(self.package_dir, 'usr', 'lib', 'boogie')

    def _create_directories(self):
        os.makedirs(self.package_dir, exist_ok=True)
        os.makedirs(self.bin_dir, exist_ok=True)
        os.makedirs(self.lib_dir, exist_ok=True)
        os.makedirs(self.meta_dir, exist_ok=True)

    def _copy_files(self):
        shutil.copy('/usr/bin/boogie', self.bin_dir)
        for file_path in glob('/usr/lib/boogie/*'):
            if file_path.endswith('z3.exe'):
                os.symlink('/usr/bin/viper-z3',
                           path.join(self.lib_dir, 'z3.exe'))
            else:
                shutil.copy(file_path, self.lib_dir)


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
                'desc': package.short_description,
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
                    debian_package = JARDebianPackage(
                            jar_path=jar_path,
                            package=package,
                            package_revision=PACKAGE_REVISION,
                            architecture=ARCHITECTURE,
                            distribution_codename=DISTRIBUTION_CODENAME,
                            maintainer=MAINTAINER,
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
    debian_packages.append(Z3DebianPackage(
        package=Z3_PACKAGE,
        package_revision=PACKAGE_REVISION,
        architecture=ARCHITECTURE,
        distribution_codename=DISTRIBUTION_CODENAME,
        maintainer=MAINTAINER,
        short_description=(
            'Z3 is a theorem prover from Microsoft Research. '
            'This package contains a Z3 version that was tested '
            'to work with Viper.'
            )
        ))
    debian_packages.append(BoogieDebianPackage(
        package=BOOGIE_PACKAGE,
        package_revision=PACKAGE_REVISION,
        architecture=ARCHITECTURE,
        distribution_codename=DISTRIBUTION_CODENAME,
        maintainer=MAINTAINER,
        short_description=(
            'Boogie is an itermediate verification language from '
            'Microsoft Research.'
            )
        ))
    debian_packages.append(ViperDebianPackage(
        debian_packages,
        package=VIPER_PACKAGE,
        package_revision=PACKAGE_REVISION,
        architecture=ARCHITECTURE,
        distribution_codename=DISTRIBUTION_CODENAME,
        maintainer=MAINTAINER,
        short_description=(
            'A meta-package for installing Viper '
            '(http://www.pm.inf.ethz.ch/research/viper.html).'
            )
        ))
    return debian_packages


def execute_scripts():
    """ Executes all generated scripts.
    """
    api_key = input(
            "If you want the packages to be uploaded to BinTray "
            "please enter your API key: ").strip()
    def run(script_name):
        print('bash', script_name, api_key)
        process = subprocess.Popen(
                ('bash', script_name, api_key),
                cwd=BUILD_DIR)
        if process.wait() != 0:
            raise Exception(script_name)
    if api_key:
        run(BUILD_SCRIPT)
        run(REPOSITORY_SETUP_SCRIPT)
        run(UPLOAD_SCRIPT)


def main():
    """ Script entry point.
    """
    global PACKAGE_REVISION
    PACKAGE_REVISION = int(input('Debian revision number: '))
    debian_packages = create_package_list()
    create_package_structures(debian_packages)
    create_build_script(debian_packages)
    create_repository_setup_script(debian_packages)
    create_upload_script(debian_packages)
    execute_scripts()


if __name__ == '__main__':
    main()
