#!/bin/bash

PIES_COLOR="\e[32m"
BARS_COLOR="\e[35m"
RESET="\e[0m"

echo -e "${PIES_COLOR}▇ Pies${RESET}     ${BARS_COLOR}▇ Bars${RESET}"
echo
probabsa/Scripts/termgraph.exe data.txt --color green,magenta --width 50