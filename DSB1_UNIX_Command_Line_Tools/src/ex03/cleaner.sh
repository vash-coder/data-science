#!/bin/sh
{
    head -n 1 ../ex02/hh_sorted.csv
    tail -n +2 ../ex02/hh_sorted.csv | gawk '
    BEGIN {
        FPAT = "([^,]+)|(\"[^\"]+\")"
        OFS = ","
    }
    {
        position_name = $3
        gsub(/^"|"$/, "", position_name)  # убираем кавычки

        levels = ""

        while (match(position_name, /(Junior|Middle|Senior)/)) {
            found_level = substr(position_name, RSTART, RLENGTH)
            levels = levels ? levels "/" found_level : found_level
            position_name = substr(position_name, RSTART + RLENGTH)
        }

        if (levels == "") levels = "-"

        $3 = "\"" levels "\""

        print
    }'
} > hh_positions.csv
