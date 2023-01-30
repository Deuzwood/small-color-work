#!/usr/bin/sh
path="src/files"

rm -rf $path
mkdir $path

# set colors to test
colors=("base" "primary" "secondary" "tertiary" "all")

# set steps to test
steps=(4 8 16 32 64)

# run luminance.py for each color and step
for color in "${colors[@]}"
do
    for step in "${steps[@]}"
    do
        python python/luminance.py -c $color -s $step -o $path/luminance_${color}_${step}
    done
done