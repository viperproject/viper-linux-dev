DOCKER_VIPER_HG_URL=https://bitbucket.org/vakaras/docker-viper-dev
SILICON_HG_URL=https://bitbucket.org/viperproject/silicon
SILVER_HG_URL=https://bitbucket.org/viperproject/silver
CHALICE2SILVER_HG_URL=https://bitbucket.org/viperproject/chalice2silver
CHALICE_HG_URL=https://bitbucket.org/viperproject/ychalice
SBT=bin/sbt
IDE=bin/ide
SUBREPOS=docker-viper silicon silver chalice2silver chalice

.PHONY: docs

test: $(SUBREPOS)
	$(SBT) test

ide: workspace $(SUBREPOS)
	$(IDE)

workspace:
	mkdir -p workspace

docs:
	cd docs/silver && make

doctest: docs/silver/build/code
	bin/doctest docs/silver/build/code

docker-viper:
	hg clone $(DOCKER_VIPER_HG_URL) docker-viper

silicon:
	hg clone $(SILICON_HG_URL) silicon

silver:
	hg clone $(SILVER_HG_URL) silver

chalice:
	hg clone $(CHALICE_HG_URL) chalice

chalice2silver:
	hg clone $(CHALICE2SILVER_HG_URL) chalice2silver

clean: clean-workspace clean-silicon clean-silicon-common clean-silver

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

clean-silver:
	rm -rf \
		silver/target silver/.classpath silver/.project silver/.settings \
		silver/project/target silver/project/project silver/.cache silver/.idea
