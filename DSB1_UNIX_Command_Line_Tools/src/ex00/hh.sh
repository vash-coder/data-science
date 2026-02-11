#!/bin/sh
vacancy=${1:-"data scientist"}
curl -G "https://api.hh.ru/vacancies" \
     --data-urlencode "text=$vacancy" \
     --data-urlencode "per_page=20" | jq . > hh.json
