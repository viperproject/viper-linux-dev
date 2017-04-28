import os
import shutil

from glob import glob
from os import path

from debian import config
from scripts.sheller import create_tool_start_script


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
                self.package_version,
                package_revision,
                )
        self.package_dir = path.join(
            config.BUILD_DIR, self.package_full_name)
        self.meta_dir = path.join(self.package_dir, 'DEBIAN')
        self.deb_path = path.join(
            config.BUILD_DIR, self.package_full_name + ".deb")
        self.deb_name = path.basename(self.deb_path)

    @property
    def package_version(self):
        return self.package.version

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
        with open(path.join(self.meta_dir, 'control'), 'wb') as fp:
            def write(field, value):
                fp.write('{0}: {1}\n'.format(field, value).encode('utf-8'))
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

    def __init__(self, jar_path, jar_version, *args, **kwargs):
        self.jar_version = jar_version
        super(JARDebianPackage, self).__init__(*args, **kwargs)
        self.section = 'java'
        self.jar_path = jar_path
        self.jar_dir = path.join(self.package_dir, 'usr', 'lib', 'viper')
        self.depends = 'default-jre'

    @property
    def package_version(self):
        return self.jar_version

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

    def __init__(self, jar_packages, binary_packages, *args, **kwargs):
        super(ViperDebianPackage, self).__init__(*args, **kwargs)
        self.section = 'base'
        self.bin_dir = path.join(self.package_dir, 'usr', 'bin')
        dependencies = [
                package.package_name
                for package in (jar_packages + binary_packages)
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
        for script_name, cls in config.TOOL_SHELL_SCRIPTS:
            script_path = path.join(self.bin_dir, script_name)
            create_tool_start_script(script_path, cls)


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
