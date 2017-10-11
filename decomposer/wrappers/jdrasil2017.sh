#!/usr/bin/env bash
kill_child_processes() {
    for childPid in $(jobs -p); do
	echo Killing $childPid
	pkill -15 -P $childPid
    done
}

trap "kill_child_processes 1 $$; echo 'Caught signal' >&2; echo 'exiting...' >&2;" SIGINT SIGTERM

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../../decomposer/latest/Jdrasil

APP_HOME="$(pwd -P)"

CLASSPATH=build/upgrades/org.sat4j.core.jar:build/jars/Jdrasil.jar
LIB_PATH="build/upgrades/"
#DEFAULT_JVM_OPTS="-XX:+UseSerialGC"
DEFAULT_JVM_OPTS="-XX:+UseG1GC"


#FOR DEBUGGING ADD
#-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005

#non-debug
call="java $DEFAULT_JVM_OPTS $JAVA_OPTS -Djava.library.path=\"$LIB_PATH\" -cp \"$CLASSPATH\" jdrasil.Exact save $TW_EXACT_OPTS "$@" < /dev/stdin"
eval $call