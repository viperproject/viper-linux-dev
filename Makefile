SBT=bin/sbt
ECLIPSE=bin/eclipse

test:
	$(SBT) test

eclipse: workspace
	$(ECLIPSE)

workspace:
	$(SBT) 'eclipse skip-parents=false'
	mkdir -p workspace

clean: clean-workspace clean-silicon clean-silicon-common clean-silver

clean-workspace:
	rm -rf \
		workspace

clean-silicon:
	rm -rf \
		silicon/tmp silicon/target silicon/.settings

clean-silicon-common:
	rm -rf \
		silicon/common/target silicon/common/.settings \
		silicon/common/.cache silicon/common/.classpath silicon/common/.project

clean-silver:
	rm -rf \
		silver/target silver/.classpath silver/.project silver/.settings \
		silver/project/target silver/project/project
