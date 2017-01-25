#!/usr/bin/env bash

PGSQL=psql
DB=nvdimp

${PGSQL} -d ${DB} -qA -t -c "SELECT * FROM nomenclature.twnamelist_floratw_view" > ../data/twnamelist.csv
${PGSQL} -d ${DB} -qA -t -c "SELECT * FROM nomenclature.twnamelist_view" > ../data/twnamelist_pg.csv
${PGSQL} -d ${DB} -qA -t -c "SELECT * FROM nomenclature.twbirdlist_view" | sed -e 's/I\ */I/g'> ../data/twbirdlist_2014.csv
${PGSQL} -d ${DB} -qA -t -c "SELECT * FROM nomenclature.jp_ylist_view" > ../data/jp_ylist.csv
