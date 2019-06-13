#!/bin/bash

for dir in $1/*; do
  echo "Extracting $dir"
  	for subdir in $dir/*; do
  		echo "Sub Directory: " $subdir
  		cd $subdir
  		python3 /Users/Isaac/SeniorProject/feature_extract.py Solution.class
  		cd -  	
  	done
  echo "Done."
done