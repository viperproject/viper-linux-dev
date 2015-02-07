SBT=bin/sbt
ECLIPSE=bin/eclipse

test:
	$(SBT) test

eclipse: workspace
	$(ECLIPSE)

workspace:
	$(SBT) eclipse skip-parents=false
	mkdir -p workspace
