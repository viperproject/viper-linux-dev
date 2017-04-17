from os import path


ROOT_DIR = '/home/developer/source'
JARS = path.join(ROOT_DIR, '*/target/universal/stage/lib/*.jar')
BUILD_DIR = path.join(ROOT_DIR, 'workspace', 'package')
MAINTAINER = 'Viper Team <viper@inf.ethz.ch>'
# TODO: Remove Bintray completely.
BINTRAY_USERNAME = 'vakaras'

TOOL_SHELL_SCRIPTS = [
    ('silicon', 'viper.silicon.SiliconRunner'),
    ('carbon', 'viper.carbon.Carbon'),
    ('chalice2silver', 'viper.chalice2sil.Program'),
    ]
