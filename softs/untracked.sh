#! /usr/bin/env bash

# Commented : how to parse both list of files with bash

# List of files tracked by git

# tracked=$(git ls-tree -t master | cut -s -f 2)

# declare -a tracked_files

# i=0
# for filename in $tracked; do
#   tracked_files[i]="$filename"

#   ((i+=1))
# done

# List of file in the same order as git ls-tree command

# output=$(LC_COLLATE=C ls -A);

# declare -a all_files

# i=0
# for filename in $output; do
#   all_files[i]="$filename"

#   ((i+=1))
# done

# ... and how to display size and contents of arrays of filenames

# printf "Nb of tracked files: %d\n" ${#tracked_files[@]}
# declare -p tracked_files

# printf "Nb of local files: %d\n" ${#all_files[@]}
# declare -p all_files

# One liner to display symmetric difference between filelists
sort <(LC_COLLATE=C ls -A) <(git ls-tree -t master | cut -s -f 2) | uniq -u

# One liner to display intersection of filelists

# sort <(LC_COLLATE=C ls -A) <(git ls-tree -t master | cut -s -f 2) | uniq -d
