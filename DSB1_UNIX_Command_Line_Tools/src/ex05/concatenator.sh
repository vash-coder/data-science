#!/bin/sh
file="hh_positions.csv"

head -n 1 *.csv | grep "," | uniq > "$file"
data=$(tail -n +2 -q *.csv)
echo "$data" >> "$file"
