#!/usr/bin/env bash

PGSQL=psql
DB=nvdimp

${PGSQL} -d ${DB} -qA -t -c "SELECT * FROM nomenclature.twnamelist_floratw_view" > ../data/twnamelist.csv
${PGSQL} -d ${DB} -qA -t -c "SELECT * FROM nomenclature.twnamelist_view" > ../data/twnamelist_apg3.csv
