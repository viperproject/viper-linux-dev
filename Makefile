DOCKER_VIPER_HG_URL=https://bitbucket.org/viperproject/viper-linux-dev-docker
SILICON_HG_URL=https://bitbucket.org/viperproject/silicon
CARBON_HG_URL=https://bitbucket.org/viperproject/carbon
SILVER_HG_URL=https://bitbucket.org/viperproject/silver
CHALICE2SILVER_HG_URL=https://bitbucket.org/viperproject/chalice2silver
ARP_PLUGIN_URL=https://bitbucket.org/viperproject/arp-plugin
ARP_PLUGIN_TEST_URL=https://bitbucket.org/viperproject/arp-plugin-test
SBT_SILICON=bin/sbt-silicon
SBT_CARBON=bin/sbt-carbon
SBT_CHALICE2SILVER=bin/sbt-chalice2silver
IDE=bin/ide
IDE_PREREQUISITES=$(SUBREPOS)
SUBREPOS=docker-viper silicon carbon silver chalice2silver arp-plugin arp-plugin-test

.PHONY: docs

test: test_silicon test_carbon test_chalice2silver

.ssh: | workspace
	mkdir .ssh
	ssh-keygen -t rsa -N "" -f .ssh/developer.key
	rm -rf workspace/.ssh
	mkdir workspace/.ssh
	chmod 700 workspace/.ssh/
	cp .ssh/developer.key.pub workspace/.ssh/authorized_keys
	chmod 600 workspace/.ssh/authorized_keys

workspace/.config/fish/config.fish: | workspace
	mkdir -p workspace/.config/fish
	echo 'set -x JAVA_TOOL_OPTIONS -Dfile.encoding=UTF8' > workspace/.config/fish/config.fish
	echo 'set -x LANG en_US.UTF-8' >> workspace/.config/fish/config.fish
	echo 'set -x LANGUAGE en_US:en' >> workspace/.config/fish/config.fish
	echo 'set -x LC_ALL en_US.UTF-8' >> workspace/.config/fish/config.fish
	echo 'set -x Z3_EXE /usr/bin/z3' >> workspace/.config/fish/config.fish
	echo 'set -x BOOGIE_EXE /usr/bin/boogie' >> workspace/.config/fish/config.fish

start_server: .ssh | $(SUBREPOS)
	bin/start-server

PORT=$(shell cat workspace/.port)
connect: .ssh workspace/.port workspace/.config/fish/config.fish
	ssh developer@localhost -p ${PORT} -i .ssh/developer.key -Y

workspace:
	mkdir -p workspace

test_silicon: $(SUBREPOS) workspace
	$(SBT_SILICON) test

test_carbon: $(SUBREPOS) workspace
	$(SBT_CARBON) test

test_chalice2silver: $(SUBREPOS) workspace
	$(SBT_CHALICE2SILVER) test

nailgun/ng:
	git clone https://github.com/martylamb/nailgun.git nailgun
	cd nailgun && make

build-standalone: $(SUBREPOS) workspace nailgun/ng
	$(SBT_CHALICE2SILVER) assembly

stage:
	$(SBT_CHALICE2SILVER) stage

package_homebrew: stage homebrew
	bin/package homebrew
	cp workspace/package/homebrew/*.rb homebrew/

homebrew:
	git clone https://github.com/vakaras/homebrew-viper.git homebrew

package_debian: stage
	bin/package debian

ide: $(IDE_PREREQUISITES) workspace
	$(IDE)

shell: workspace
	bin/shell

docs:
	cd docs/silver && make

build_image: $(SUBREPOS)
	cd docker-viper/ && ./build

doctest: docs/silver/build/code
	bin/doctest docs/silver/build/code

docker-viper:
	hg clone $(DOCKER_VIPER_HG_URL) docker-viper

silicon:
	hg clone $(SILICON_HG_URL) silicon

carbon:
	hg clone $(CARBON_HG_URL) carbon

silver:
	hg clone $(SILVER_HG_URL) silver

chalice2silver:
	hg clone $(CHALICE2SILVER_HG_URL) chalice2silver

arp-plugin:
	hg clone $(ARP_PLUGIN_URL) arp-plugin

arp-plugin-test:
	hg clone $(ARP_PLUGIN_TEST_URL) arp-plugin-test

clean: clean-workspace clean-silicon clean-carbon clean-silicon-common clean-silver
	rm -rf .cache

clean-workspace:
	rm -rf \
		workspace

clean-silicon:
	rm -rf \
		silicon/tmp silicon/target silicon/.settings \
		silicon/.classpath silicon/.project \
		silicon/.idea silicon/.idea_modules \
		silicon/project/target silicon/project/.ivy silicon/project/.boot \
		silicon/project/project silicon/projectFilesBackup

clean-silicon-common:
	rm -rf \
		silicon/common/target silicon/common/.settings \
		silicon/common/.cache silicon/common/.classpath silicon/common/.project

clean-carbon:
	rm -rf \
		carbon/tmp carbon/target carbon/.settings \
		carbon/.classpath carbon/.project \
		carbon/.idea carbon/.idea_modules \
		carbon/project/target carbon/project/.ivy carbon/project/.boot \
		carbon/project/project carbon/projectFilesBackup

clean-silver:
	rm -rf \
		silver/target silver/.classpath silver/.project silver/.settings \
		silver/project/target silver/project/project silver/.cache silver/.idea
