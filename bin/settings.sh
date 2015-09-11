#!/bin/bash

export BIN_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export ROOT_DIR="${BIN_DIR}/.."
export WORKSPACE_DIR="${ROOT_DIR}/workspace"
export NAILGUN_BIN="${ROOT_DIR}/nailgun/ng"
export NAILGUN_SERVER_BIN="${BIN_DIR}/nailgun-server"
export DOCKER_HOME=/home/developer
export DOCKER_SOURCE_DIR="$DOCKER_HOME/source"
export DOCKER_SBT="sbt"
export DOCKER_IMAGE="vakaras/viper-build:0.0.11"
export DOCKER_DEFAULT_MOUNT="\
  -v ${WORKSPACE_DIR}:${DOCKER_HOME} \
  -v ${ROOT_DIR}:${DOCKER_SOURCE_DIR}"
export DOCKER_COMMAND="docker run --rm -ti ${DOCKER_DEFAULT_MOUNT}"
export DOCKER_COMMAND_DETTACHED="docker run -d ${DOCKER_DEFAULT_MOUNT}"
export DOCKER_NAILGUN_SERVER_NAME="viper-nailgun-server"
export HOST_SILVER_FILE_PATH="${WORKSPACE_DIR}/program.sil"
export DOCKER_SILVER_FILE_PATH="${DOCKER_HOME}/program.sil"
export HOST_ERROR_FILE_PATH="${WORKSPACE_DIR}/errors.log"
export DOCKER_ERROR_FILE_PATH="${DOCKER_HOME}/errors.log"
export SILICON_MAIN_CLASS=viper.silicon.SiliconRunner
