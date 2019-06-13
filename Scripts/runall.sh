#!/bin/bash

CWD=`pwd`

for challenge in $1/*; do
  for dir in $challenge/*; do
    cd $dir
    $CWD/runtest.sh
    cd $CWD
  done
done
