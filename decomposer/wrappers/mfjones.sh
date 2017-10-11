#!/bin/bash

# Contributors: Serge Gaspers, Joachim Gudmundsson, Mitchell Jones,
#               Julian Mestre, Stefan Rummele.
# License: This source code is distributed under the open source MIT license.

# Purpose: In some cases the JVM can take a few moments to startup, however we
# must still handle the SIGUSR1 and SIGTERM signals appropriately. This script
# sets temporary traps so that SIGUSR1 and SIGTERM still prints out the
# information required.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../../decomposer/pace2016/mfjones/

if [[ "$1" == "--help" || "$1" == "-h" ]]
then
  echo "Usage:"
  echo "  $0 [-s seed]"
  echo ""
  echo "Data must be passed via stdin."
  echo "Example: $0 -s 4321 < example.gr"
  exit 0
fi

# Reset getopts.
OPTIND=1
seed=""

while getopts ":s:" opt; do
  case "$opt" in
    s)
      seed=$OPTARG
      ;;
  esac
done

# Copy the input to shared memory.
shmdir="/dev/shm/"
name="input_tmpfile"
tmp="$shmdir$name"_"$$"
trap 'rm -f $tmp' EXIT
cat > $tmp

# Temporary traps while we wait for Java, output a tree decomposition
# of width equal to the number of vertices (i.e. all nodes in a single bag).
nodes=$(head -n1 $tmp | cut -d ' ' -f 3)

# Pass the input from shm to Java.
java -Xmx10g Main -s $seed < $tmp &
PID=$!

trivialTree() {
  kill -SIGKILL $PID &> /dev/null
  echo "s td 1 $nodes $nodes"
  echo "b 1" "$(seq -s ' ' 1 $nodes)"
  exit 0
}

trap trivialTree SIGTERM

# Wait 0.5s for the JVM to boot up.
for i in {1..50}
do
  sleep 0.01
done

# The actual traps, forward the signals to the JVM.
trap "kill -SIGTERM $PID" SIGTERM
trap "kill -SIGKILL -- -$PID &> /dev/null; rm -f $tmp" EXIT

while :
do
  # Wait for child process, signals interrupt this!
  wait $PID

  # If child process is no longer active, abort.
  kill -0 $PID 2> /dev/null || break
done
