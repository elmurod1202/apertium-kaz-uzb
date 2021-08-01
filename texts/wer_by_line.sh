#!/bin/bash
# Reads uzb-big and kaz-uzb files line by line
# Calculates WER per line
# Sorts by WER score in descending order to show what sentences are causeing the most problem.

# Reading both files line by line at once:
count=0
declare -a lines
while IFS= read -r line_test && IFS= read -r line_ref <&3; do
    count=$((count+1))
    # Saving each line in a separate file so the apertium-eval can read it:
    echo $line_test  > tmp.test
    echo $line_ref  > tmp.ref
    wer=$(apertium-eval-translator -ref tmp.ref -test tmp.test | grep -F "Word error rate (WER):" | head -1 | awk -F" " '{print $5}')
    echo "$count: $wer"
    line="$wer% $line_test"
    lines[$count]=$line
    # echo ${lines[$count]}
    # exit
done < kaz-uzb.txt 3< uzb-big.txt

rm tmp.test
rm tmp.ref

# Sorting the array:
readarray -t sorted_lines < <(for a in "${lines[@]}"; do echo "$a"; done | sort -r)

# Saving the array in a file:
rm wer_lines.txt
for a in "${sorted_lines[@]}" 
do
    echo "$a" >> wer_lines.txt
done
echo "Results saved in wer_lines.txt"
echo "Done."