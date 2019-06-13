#!/bin/bash

for dir in $1/*; do
  echo "Getting pairs from: $dir"
  	for subdir in $dir/*; do
  		echo "Sub Directory: " $subdir
  		cd $subdir
  		rm X3.csv
  		rm Y3.csv
  		python3 ../../../../../get_pairs.py code.csv -n $2
  		cd -  	
  	done
  echo "Done."
done