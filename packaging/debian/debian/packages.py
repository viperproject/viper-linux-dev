import os
import shutil

from glob import glob
from os import path

from debian import config


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
        self.package_dir = path.join(
            config.BUILD_DIR, self.package_full_name)
        self.meta_dir = path.join(self.package_dir, 'DEBIAN')
        self.deb_path = path.join(
            config.BUILD_DIR, self.package_full_name + ".deb")
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
                fp.write(r'''#!/bin/bash
USE_NAILGUN=false
IDE_MODE=false
SILVER_FILE_PATH=
OPTS=

JAVA=java
JAVA_ARGS=-Xss30M
NAILGUN_JAR=/usr/share/java/nailgun-0.9.0.jar:/usr/share/java/nailgun-server.jar
NAILGUN_MAIN=com.martiansoftware.nailgun.NGServer
NAILGUN_PID_FILE=/tmp/viper_nailgun.pid
NAILGUN_OUT_FILE=/tmp/viper_nailgun.out
NAILGUN_BIN=ng-nailgun
IDE_ERROR_FILE=/tmp/viper_ide.err
IDE_OUTPUT_FILE=/tmp/viper_ide.out

JARS=($(ls /usr/lib/viper/*.jar))
CP=$(printf ":%s" "${{JARS[@]}}")
CP=${{CP:1}}
export Z3_EXE=/usr/bin/viper-z3
export BOOGIE_EXE=/usr/bin/boogie

# https://stackoverflow.com/a/14203146
while [[ $# > 0 ]]
do
  key="$1"

  case $key in
    --help)
      OPTS="$OPTS --help"
    ;;
    --useNailgun)
      USE_NAILGUN=true
    ;;
    --ideMode)
      IDE_MODE=true
    ;;
    --*)
      value="$2"
      OPTS="$OPTS $key $value"
      shift
    ;;
    *)
      SILVER_FILE_PATH="$key"
    ;;
  esac
  shift
done

function start-nailgun() {{
  $JAVA $JAVA_ARGS -cp "$1" "$NAILGUN_MAIN" &
}}

if [[ "$USE_NAILGUN" == "true" ]]; then
  if [ ! -f "$NAILGUN_PID_FILE" ]; then
    # Start nailgun.
    CP="$CP:$NAILGUN_JAR"
    start-nailgun "$CP" &> "$NAILGUN_OUT_FILE"
    touch "$NAILGUN_PID_FILE"
  fi
  if [[ "$IDE_MODE" == "true" ]]; then
    echo "" > "$IDE_OUTPUT_FILE"
    ng-nailgun {main_class} $OPTS \
            --ideMode --ideModeErrorFile "$IDE_OUTPUT_FILE" \
            "$SILVER_FILE_PATH" &> "$IDE_ERROR_FILE"
    RETURN_CODE=$?
    cat "$IDE_OUTPUT_FILE"
    cat "$IDE_ERROR_FILE" 1>&2
    exit $RETURN_CODE
  else
    ng-nailgun {main_class} $OPTS "$SILVER_FILE_PATH"
  fi
else
  if [[ "$IDE_MODE" == "true" ]]; then
    echo "" > "$IDE_OUTPUT_FILE"
    $JAVA $JAVA_ARGS -cp "$CP" {main_class} $OPTS \
            --ideMode --ideModeErrorFile "$IDE_OUTPUT_FILE" \
            "$SILVER_FILE_PATH" &> "$IDE_ERROR_FILE"
    RETURN_CODE=$?
    cat "$IDE_OUTPUT_FILE"
    cat "$IDE_ERROR_FILE" 1>&2
    exit $RETURN_CODE
  else
    $JAVA $JAVA_ARGS -cp "$CP" {main_class} $OPTS "$SILVER_FILE_PATH"
  fi
fi
                '''.format(
                    main_class=cls,
                    )
                )
            os.chmod(script_path, 0o755)


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
