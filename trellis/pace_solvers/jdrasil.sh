#!/usr/bin/env bash
#!/usr/bin/env bash
kill_child_processes() {
    for childPid in $(jobs -p); do
	echo Killing $childPid
	pkill -15 -P $childPid
	#kill -15 $childPid
    done
}

trap "kill_child_processes 1 $$; echo 'Caught signal' >&2; echo 'exiting...' >&2;" SIGINT SIGTERM

cd ~/src/treewidth-portfolio/solvers/exact/jdrasil/jdrasil/src

#debug
#java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -cp ../../lib/glucose.jar:../../lib/glucosep.jar:../../lib/pblib.jar:. -Djava.library.path=../../lib/glucose/simp/:../../lib/glucose/parallel:../../lib/pblib de.uniluebeck.tcs.App "$@" < /dev/stdin
#non-debug
java -cp ../../lib/glucose.jar:../../lib/glucosep.jar:../../lib/pblib.jar:. -Djava.library.path=../../lib/glucose/simp/:../../lib/glucose/parallel:../../lib/pblib de.uniluebeck.tcs.App "$@" < /dev/stdin
