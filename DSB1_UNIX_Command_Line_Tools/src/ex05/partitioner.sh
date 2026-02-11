#!/bin/sh
file="../ex03/hh_positions.csv"
header=$(head -n 1 "$file")

tail -n +2 "$file" | awk -F ',' -v header="$header" '
{
    date = substr($2, 2, 10)
    file = date ".csv"
    if (!(date in seen)) {
        print header > file
        seen[date] = 1
    }
    print >> file
}'