#!/usr/bin/env bash
kill_child_processes() {
    for childPid in $(jobs -p); do
	echo Killing $childPid
	pkill -15 -P $childPid
    done
}

trap "kill_child_processes 1 $$; echo 'Caught signal' >&2; echo 'exiting...' >&2;" SIGINT SIGTERM

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../../decomposer/latest/tamaki/

#debug
#java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -Xmx4g -Xms4g -Xss10m tw.exact.MainDecomposer < /dev/stdin


#non-debug
java -Xmx4g -Xms4g -Xss10m tw.exact.MainDecomposer < /dev/stdin

