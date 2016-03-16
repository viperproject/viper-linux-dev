from os import path


ROOT_DIR = '/home/developer/source'
JARS_DIR = path.join(
    ROOT_DIR, 'chalice2silver/target/universal/stage/lib')
JARS = path.join(JARS_DIR, '*.jar')
BUILD_DIR = path.join(ROOT_DIR, 'workspace', 'package')
#MAINTAINER = 'Viper Team <viper@inf.ethz.ch>'
MAINTAINER = 'Vytautas Astrauskas <vastrauskas@gmail.com>'
BINTRAY_USERNAME = 'vakaras'

TOOL_SHELL_SCRIPTS = [
    ('silicon', 'viper.silicon.SiliconRunner'),
    ('carbon', 'viper.carbon.Carbon'),
    ('chalice2silver', 'viper.chalice2sil.Program'),
    ]
