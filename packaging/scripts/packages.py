#!/usr/bin/python3


from scripts.utils import Package
from scripts.licenses import LICENSES

Z3_PACKAGE = Package(' # z3 # 4.4.0', LICENSES['MIT'], 'https://github.com/Z3Prover/z3')
BOOGIE_PACKAGE = Package(' # boogie # 2015.06.10', LICENSES['Ms-PL'], 'https://github.com/boogie-org/boogie')
VIPER_PACKAGE = Package(' # viper # 0.1', LICENSES['MPL'], 'https://bitbucket.org/viperproject/viper-linux-dev')

PACKAGES = [
        Package('com.google.code.findbugs # jsr305 # 2.0.3', LICENSES['LGPL2.1'], 'https://github.com/findbugsproject/findbugs/', omit=True),
        Package('log4j # log4j # 1.2.17', LICENSES['APACHE'], 'https://git-wip-us.apache.org/repos/asf?p=logging-log4j2.git;a=summary'),
        Package('org.scalatest # scalatest_2.11 # 2.2.1', LICENSES['APACHE'], omit=True),
        Package('org.scala-lang # scala-library # 2.11.7', LICENSES['BSD-scala'], 'https://github.com/scala/scala'),
        Package('org.scala-lang # scala-reflect # 2.11.6', LICENSES['BSD-scala'], 'https://github.com/scala/scala'),
        Package('org.scala-lang.modules # scala-parser-combinators_2.11 # 1.0.2', LICENSES['BSD-scala'], 'https://github.com/scala/scala-parser-combinators'),
        Package('org.scala-lang.modules # scala-xml_2.11 # 1.0.2', LICENSES['BSD-scala'], 'https://github.com/scala/scala-xml'),
        Package('jline # jline # 2.12', LICENSES['BSD'], omit=True),
        Package('org.jgrapht # jgrapht-core # 0.9.0', LICENSES['EPL'], 'https://github.com/jgrapht/jgrapht'),
        Package('com.googlecode.kiama # kiama_2.11 # 1.8.0', LICENSES['LGPL3.0'], 'https://bitbucket.org/inkytonik/kiama'),
        Package('org.bitbucket.inkytonik.dsinfo # dsinfo_2.11 # 0.4.0', LICENSES['LGPL3.0'], omit=True),
        Package('org.bitbucket.inkytonik.dsprofile # dsprofile_2.11 # 0.4.0', LICENSES['LGPL3.0'], omit=True),
        Package('org.slf4s # slf4s-api_2.11 # 1.7.12', LICENSES['MIT'], 'https://github.com/mattroberts297/slf4s'),
        Package('org.slf4j # slf4j-api # 1.7.12', LICENSES['MIT'], 'https://github.com/qos-ch/slf4j'),
        Package('org.slf4j # slf4j-log4j12 # 1.7.12', LICENSES['MIT'], 'https://github.com/qos-ch/slf4j'),
        Package('com.github.scopt # scopt_2.11 # 3.2.0', LICENSES['MIT'], 'https://github.com/scopt/scopt'),
        Package('org.rogach # scallop_2.11 # 0.9.5', LICENSES['MIT'], 'https://github.com/scallop/scallop'),
        Package('com.google.guava # guava # 17.0', LICENSES['APACHE'], 'https://github.com/google/guava'),
        Package('com.lihaoyi # fastparse # 0.3.7', LICENSES['MIT'], 'https://github.com/lihaoyi/fastparse'),
        Package('com.lihaoyi # sourcecode # 0.1.1', LICENSES['MIT'], 'https://github.com/lihaoyi/sourcecode'),
        Package('commons-io # commons-io # 2.4', LICENSES['APACHE'], 'https://commons.apache.org/proper/commons-io/source-repository.html'),
        Package('org.apache.commons # commons-pool2 # 2.4', LICENSES['APACHE'], 'https://commons.apache.org/proper/commons-pool/source-repository.html'),
        Package('viper # silicon-common # 0.1-SNAPSHOT', LICENSES['MPL'], 'https://bitbucket.org/viperproject/silicon/'),
        Package('viper # silicon # 0.1-SNAPSHOT', (LICENSES['MPL'], LICENSES['Ms-PL']), 'https://bitbucket.org/viperproject/silicon/'),
        Package('viper # silver # 0.1-SNAPSHOT', LICENSES['MPL'], 'https://bitbucket.org/viperproject/silver/'),
        Package('viper # chalice2sil # 0.1-SNAPSHOT', (LICENSES['MPL'], LICENSES['Ms-PL']), 'https://bitbucket.org/viperproject/chalice2silver/'),
        Package('viper # carbon # 1.0-SNAPSHOT', LICENSES['MPL'], 'https://bitbucket.org/viperproject/carbon'),
        Z3_PACKAGE,
        BOOGIE_PACKAGE,
        ]
