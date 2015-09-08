#!/bin/bash

export BIN_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export ROOT_DIR="${BIN_DIR}/.."
export DOCKER_HOME=/home/developer
export DOCKER_SOURCE_DIR="$DOCKER_HOME/source"
export DOCKER_SBT="sbt"
export DOCKER_IMAGE="vakaras/viper-build:0.0.7"
export DOCKER_DEFAULT_MOUNT="\
  -v ${ROOT_DIR}/workspace:${DOCKER_HOME} \
  -v ${ROOT_DIR}:${DOCKER_SOURCE_DIR}"
export DOCKER_COMMAND="docker run --rm -ti ${DOCKER_DEFAULT_MOUNT}"
