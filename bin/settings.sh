#!/bin/bash

# https://bosker.wordpress.com/2012/02/12/bash-scripters-beware-of-the-cdpath/
unset CDPATH

# https://stackoverflow.com/a/246128
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done

export BIN_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
export ROOT_DIR="${BIN_DIR}/.."
export WORKSPACE_DIR="${ROOT_DIR}/workspace"
export NAILGUN_BIN="${ROOT_DIR}/nailgun/ng"
export NAILGUN_SERVER_BIN="${BIN_DIR}/nailgun-server"
function docker_run_fun () {
  if [[ $(uname) != 'Darwin' ]]; then
    if [ "$EUID" -ne 0 ]; then
      >&2 echo 'To start a Docker container, you need to be root.'
      >&2 echo 'Using sudo to get root permissions.'
      CMD="sudo docker"
    else
      CMD="docker"
    fi
  else
    CMD="docker"
  fi
  ${CMD} $@
}
export DOCKER_BIN="docker_run_fun"
export DOCKER_HOME=/home/developer
export DOCKER_SOURCE_DIR="$DOCKER_HOME/source"
export DOCKER_SBT="sbt"
export DOCKER_IMAGE="vakaras/viper-build:0.0.11"
export DOCKER_DEFAULT_MOUNT="\
  -v ${WORKSPACE_DIR}:${DOCKER_HOME} \
  -v ${ROOT_DIR}:${DOCKER_SOURCE_DIR}"
export DOCKER_COMMAND="${DOCKER_BIN} run --rm -ti ${DOCKER_DEFAULT_MOUNT}"
export DOCKER_COMMAND_DETTACHED="${DOCKER_BIN} run -d ${DOCKER_DEFAULT_MOUNT}"
export DOCKER_NAILGUN_SERVER_NAME="viper-nailgun-server"
export HOST_SILVER_FILE_PATH="${WORKSPACE_DIR}/program.sil"
export DOCKER_SILVER_FILE_PATH="${DOCKER_HOME}/program.sil"
export HOST_ERROR_FILE_PATH="${WORKSPACE_DIR}/errors.log"
export DOCKER_ERROR_FILE_PATH="${DOCKER_HOME}/errors.log"
export SILICON_MAIN_CLASS=viper.silicon.SiliconRunner
export CARBON_MAIN_CLASS=viper.carbon.Carbon
