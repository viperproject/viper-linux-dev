SBT=bin/sbt
IDE=bin/ide

test:
	$(SBT) test

ide: workspace
	$(IDE)

workspace:
	mkdir -p workspace

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
