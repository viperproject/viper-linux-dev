import os


def create_tool_start_script(script_path, main_class):
    with open(script_path, 'w') as fp:
        fp.write(r'''#!/bin/bash
USE_NAILGUN=false
IDE_MODE=false
SILVER_FILE_PATH=
OPTS=

JAVA=java
JAVA_ARGS=-Xss30M
NAILGUN_JAR=/usr/share/java/nailgun-0.9.0.jar:/usr/share/java/nailgun-server.jar
NAILGUN_MAIN=com.martiansoftware.nailgun.NGServer
NAILGUN_PID_FILE=/tmp/viper_nailgun.pid
NAILGUN_OUT_FILE=/tmp/viper_nailgun.out
NAILGUN_BIN=ng-nailgun
IDE_ERROR_FILE=/tmp/viper_ide.err
IDE_OUTPUT_FILE=/tmp/viper_ide.out

JARS=($(ls /usr/lib/viper/*.jar))
CP=$(printf ":%s" "${{JARS[@]}}")
CP=${{CP:1}}
export Z3_EXE=/usr/bin/viper-z3
export BOOGIE_EXE=/usr/bin/boogie

# https://stackoverflow.com/a/14203146
while [[ $# > 0 ]]
do
  key="$1"

  case $key in
    --help)
      OPTS="$OPTS --help"
    ;;
    --useNailgun)
      USE_NAILGUN=true
    ;;
    --ideMode)
      IDE_MODE=true
    ;;
    --*)
      value="$2"
      OPTS="$OPTS $key $value"
      shift
    ;;
    *)
      SILVER_FILE_PATH="$key"
    ;;
  esac
  shift
done

function start-nailgun() {{
  $JAVA $JAVA_ARGS -cp "$1" "$NAILGUN_MAIN" &
}}

if [[ "$USE_NAILGUN" == "true" ]]; then
  if [ ! -f "$NAILGUN_PID_FILE" ]; then
    # Start nailgun.
    CP="$CP:$NAILGUN_JAR"
    start-nailgun "$CP" &> "$NAILGUN_OUT_FILE"
    touch "$NAILGUN_PID_FILE"
  fi
  if [[ "$IDE_MODE" == "true" ]]; then
    echo "" > "$IDE_OUTPUT_FILE"
    $NAILGUN_BIN {main_class} $OPTS \
            --ideMode --ideModeErrorFile "$IDE_OUTPUT_FILE" \
            "$SILVER_FILE_PATH" &> "$IDE_ERROR_FILE"
    RETURN_CODE=$?
    cat "$IDE_OUTPUT_FILE"
    cat "$IDE_ERROR_FILE" 1>&2
    exit $RETURN_CODE
  else
    $NAILGUN_BIN {main_class} $OPTS "$SILVER_FILE_PATH"
  fi
else
  if [[ "$IDE_MODE" == "true" ]]; then
    echo "" > "$IDE_OUTPUT_FILE"
    $JAVA $JAVA_ARGS -cp "$CP" {main_class} $OPTS \
            --ideMode --ideModeErrorFile "$IDE_OUTPUT_FILE" \
            "$SILVER_FILE_PATH" &> "$IDE_ERROR_FILE"
    RETURN_CODE=$?
    cat "$IDE_OUTPUT_FILE"
    cat "$IDE_ERROR_FILE" 1>&2
    exit $RETURN_CODE
  else
    $JAVA $JAVA_ARGS -cp "$CP" {main_class} $OPTS "$SILVER_FILE_PATH"
  fi
fi
        '''.format(
            main_class=main_class,
            )
        )
        os.chmod(script_path, 0o755)
