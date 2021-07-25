#!/bin/bash
# Reads uzb-big and kaz-uzb files line by line
# Calculates WER per line
# Sorts by WER score in descending order to show what sentences are causeing the most problem.

while IFS= read -r line1 && IFS= read -r line2 <&3; do
  echo "File 1: $line_test"
  echo "File 2: $line_ref"
done < kaz-uzb.txt 3< uzb-big.txt