import subprocess

from os import path

from brew import config


class HomebrewFormula:
    
    def __init__(self, name, directory, homepage, url, version=None):
        self.name = name
        self.directory = directory
        self.homepage = homepage
        self.url = url
        self.version = version

        self.class_name = ''.join(
            part.title()
            for part in self.name.split('-'))
        self.path = path.join(self.directory, self.name + '.rb')
        self.dependencies = []
        self.install_blocks = []
        self.resources = []

    def add_dependency(self, name):
        self.dependencies.append(name)

    def add_install_block(self, block):
        self.install_blocks.append(block)

    def add_resource(self, name, url, sha256):
        self.resources.append((name, url, sha256))

    def write(self):
        with open(self.path, 'w') as fp:
            indent = 0
            def wl(s, *args, **kwargs):
                fp.write(
                    ('  ' * indent) +
                    s.format(*args, **kwargs) +
                    '\n')
            def wn():
                fp.write('\n')
            def wrl(line):
                fp.write(line + '\n')
            def wp(key, value):
                wl('{} "{}"', key, value)
            def begin(s, *args, **kwargs):
                wl(s, *args, **kwargs)
                nonlocal indent
                indent += 1
            def end():
                nonlocal indent
                indent -= 1
                wl('end')

            wl('require "formula"')
            begin('class {} < Formula', self.class_name)

            wp('homepage', self.homepage)
            wp('url', self.url)
            if self.version:
                wp('version', self.version)
            wn()

            for dependency in self.dependencies:
                wp('depends_on', dependency)
            wn()

            for name, url, sha256 in self.resources:
                begin('resource "{}" do', name)
                wp('url', url)
                wp('sha256', sha256)
                end()

            begin('def install')
            for block in self.install_blocks:
                for line in block.splitlines():
                    if not line.isspace():
                        wrl(line)
            end()
            
            end()


class HomebrewPackage:
    """ A Homebrew package.

    This class implements method template design pattern.
    """

    def __init__(self,
            package,
            package_revision,
            short_description):

        self.package = package
        self.package_revision = package_revision
        self.short_description = short_description
        self.full_version = "{0}-{1}".format(
                self.package_version,
                package_revision,
                )

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
        """ Creates files needed to create a package.
        """

    def get_download_url(self):
        """ Returns the url from which the file can be downloaded.
        """
        return "https://bintray.com/artifact/download/{}/{}/{}".format(
            config.BINTRAY_USERNAME,
            config.REPOSITORY_NAME,
            self.file_name,
            )

    @property
    def file_name(self):
        raise NotImplementedError()


class JARHomebrewPackage(HomebrewPackage):
    """ A Homebrew package encapsulating JAR file.
    """

    def __init__(self, jar_path, jar_version, *args, **kwargs):
        self.jar_version = jar_version
        super(JARHomebrewPackage, self).__init__(*args, **kwargs)
        self.jar_path = jar_path

    @property
    def package_version(self):
        return self.jar_version

    @property
    def file_name(self):
        return self.package_full_name + '.jar'

    def get_sha256(self):
        output = subprocess.check_output(['sha256sum', self.jar_path])
        return output.decode('utf-8').split()[0]


class Z3HomebrewPackage(HomebrewPackage):
    """ A Homebrew package for Z3.
    """

    def create_package_structure(self):
        """ Creates files needed to create a package.
        """

        formula = HomebrewFormula(
            name='viper-z3', 
            directory=config.BUILD_DIR,
            homepage="https://github.com/Z3Prover/z3",
            url="https://github.com/Z3Prover/z3/archive/z3-4.4.0.tar.gz",
            )
        formula.add_dependency('python')
        formula.add_install_block(r'''
    system "python", "scripts/mk_make.py", "--prefix=#{prefix}"
    Dir.chdir "build" do
      system "make"
      system "make", "PREFIX=#{prefix}", "install"
    end''')
        formula.write()


class BoogieHomebrewPackage(HomebrewPackage):
    """ A Homebrew package for Boogie.
    """

    def create_package_structure(self):
        """ Creates files needed to create a package.
        """

        formula = HomebrewFormula(
            name='boogie', 
            directory=config.BUILD_DIR,
            homepage="http://boogie.codeplex.com",
            url="https://github.com/boogie-org/boogie.git",
            version="2.3",
            )
        formula.add_dependency('mono')
        formula.add_install_block(r'''
    system "curl", "-L", "-o", "nuget.exe", "https://nuget.org/nuget.exe"
    system "mono", "nuget.exe", "restore", "./Source/Boogie.sln"
    system "xbuild", "Source/Boogie.sln"
    system "mkdir", "#{prefix}/Binaries"
    system "cp", "-r", "Binaries/", "#{prefix}/Binaries"
    system "echo '#!/bin/sh'$'\\n''mono\ #{prefix}/Binaries/Boogie.exe\ \"$@\"'$'\\n' > #{prefix}/Binaries/boogie"
    system "chmod", "+x", "#{prefix}/Binaries/boogie"
    ''')
        formula.write()


class ViperHomebrewPackage(HomebrewPackage):
    """ A package that has a dependency on all other packages.

    Also it contains shell scripts for invocation.
    """

    def __init__(self, jar_packages, binary_packages, *args, **kwargs):
        super(ViperHomebrewPackage, self).__init__(*args, **kwargs)
        self.jar_packages = jar_packages
        self.binary_packages = binary_packages

    @property
    def package_name(self):
        return 'viper'

    @property
    def file_name(self):
        return self.package_full_name + '.tar.gz'

    def create_package_structure(self):
        """ Creates files needed to create a package.
        """
        self.create_formula()
        #self.create_archive()

    def create_formula(self):
        """ Creates Homebrew formula.
        """
        formula = HomebrewFormula(
            name='viper', 
            directory=config.BUILD_DIR,
            homepage="http://www.pm.inf.ethz.ch/research/viper.html",
            url=self.get_download_url(),
            )

        formula.add_dependency('nailgun')
        formula.add_dependency('boogie')
        formula.add_dependency('viper-z3')

        for jar_package in self.jar_packages:
            formula.add_resource(
                jar_package.package_name,
                jar_package.get_download_url(),
                jar_package.get_sha256())

        for script_name, cls in config.TOOL_SHELL_SCRIPTS:
            formula.add_install_block(r'''
    inreplace "{0}", "/usr/lib/viper", "#{{prefix}}"
    inreplace "{0}", "/usr/bin/viper-z3", "/usr/local/bin/z3"
    inreplace "{0}", "/usr/bin/boogie", "/usr/local/bin/boogie"
    inreplace "{0}", "NAILGUN_BIN=ng-nailgun", "NAILGUN_BIN=ng"
    inreplace "{0}", "NAILGUN_JAR=", "NAILGUN_JAR=/usr/local/Cellar/nailgun/0.9.1/libexec/nailgun-server-0.9.1.jar:"
    bin.install "{0}"
            '''.format(script_name))
        for jar_package in self.jar_packages:
            formula.add_install_block(r'''
    prefix.install resource("{0}")
                '''.format(jar_package.package_name,))
        formula.write()
