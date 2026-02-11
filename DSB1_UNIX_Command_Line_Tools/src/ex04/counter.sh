#!/bin/sh
{
    echo "\"name\",\"count\""
    tail -n +2 ../ex03/hh_positions.csv \
    | awk -F',' '
        {
            name = $3
            gsub(/"/, "", name)
            if (name != "-") {
                count[name]++
            }
        }
        END {
            for (i in count) {
                print "\"" i "\"," count[i]
            }
        }
    ' | sort -t',' -k2,2nr
} > hh_uniq_positions.csv
