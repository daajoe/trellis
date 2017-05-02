#!/usr/bin/env bash
cat $1 | sed '/^\s*$/d;/^c/ d;/^p/ d;s/[[:blank:]]*$//;s/e /edge(/;s/ /,/g' | awk '{print $0")."}' | sed '/^\s*$/d'
