#!/usr/bin/env bash
kill_child_processes() {
    for childPid in $(jobs -p); do
	echo Killing $childPid
	pkill -15 -P $childPid
    done
}

trap "kill_child_processes 1 $$; echo 'Caught signal' >&2; echo 'exiting...' >&2;" SIGINT SIGTERM

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../../decomposer/pace2016/htd/

LD_LIBRARY_PATH=$DIR $DIR/htd_main "$@" < /dev/stdin
