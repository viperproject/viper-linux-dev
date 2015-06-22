#!/bin/bash

export BIN_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export ROOT_DIR="${BIN_DIR}/.."
export DOCKER_HOME=/home/developer
export DOCKER_DEFAULT_MOUNT="\
  -v ${ROOT_DIR}/.cache/ivy2:${DOCKER_HOME}/.ivy2 \
  -v ${ROOT_DIR}/.cache/sbt:${DOCKER_HOME}/.sbt \
  -v ${ROOT_DIR}/.cache/IdeaIC14:${DOCKER_HOME}/.IdeaIC14"
export DOCKER_COMMAND="docker run --rm -ti ${DOCKER_DEFAULT_MOUNT}"
export DOCKER_SOURCE_DIR="$DOCKER_HOME/source"
export DOCKER_SBT="sbt"
export DOCKER_IMAGE="vakaras/viper-build:0.0.5"
