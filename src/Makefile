PYUIC=pyuic5
PYRCC=pyrcc5
PYTHON=python3
PYTHONVENV=PYTHON36
PYINSTALLER=$(PYTHONVENV)/bin/pyinstaller
VERSION=v0.5.2
#PYINSTALLER= /usr/local/bin/pyinstaller

all: mui translate binary

mui:
	$(PYUIC) ui/ui_main.ui -o ui_main.py
	$(PYUIC) ui/ui_about.ui -o ui_about.py
	$(PYUIC) ui/ui_combine.ui -o ui_combine.py
	$(PYUIC) ui/ui_compare.ui -o ui_compare.py
	$(PYUIC) ui/ui_format.ui -o ui_format.py
	$(PYUIC) ui/ui_databases.ui -o ui_databases.py
	$(PYRCC) -o iconResources_rc.py iconResources.qrc

translate:
	./make_trans_ui.sh

binary:
	$(PYINSTALLER) --onefile checklister.spec --clean
	rm -fr /Applications/checklister.app
	cp -rf dist/checklister.app /Applications/; cp -rf dist/checklister.app ../../packages/
	rm -fr dist/checklister_dist
	mkdir -p dist/checklister_dist
	mv dist/checklister.app dist/checklister_dist
	hdiutil create dist/checklister.dmg -srcfolder dist/checklister_dist -ov


create_db_schema:
	rm db/twnamelist.db
	sqlite3 db/twnamelist.db < db_schema/pnamelist.sql

update_db:
	# export pgsql view to csv files
	./exp_twnamelist_view.sh
	sed -e 's/'\''/'\'\''/g' ../data/twnamelist_pg.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_pnamelist_pg (id,family,family_cname,cname,name,fullname,plant_type,endemic,iucn_category,source) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","q$$6q","$$7","$$8","q$$9q","q$$10q");"}' > db_schema/insert_pnamelist_pg.sql
	sed -e 's/'\''/'\'\''/g' ../data/twredlist2017.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_twredlist2017 (id,family,family_cname,cname,name,fullname,plant_type,endemic,iucn_category,source) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","q$$6q","$$7","$$8","q$$9q","q$$10q");"}' > db_schema/insert_twredlist2017.sql
	sed -e 's/'\''/'\'\''/g' ../data/twnamelist_pg_synonym.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_pnamelist_pg_synonym (id,accepted_namecode,namecode,fullname,cname,synonyms) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","q$$6q");"}' > db_schema/insert_pnamelist_pg_synonym.sql
	sed -e 's/'\''/'\'\''/g' ../data/twnamelist.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_pnamelist (id,family,family_cname,cname,name,fullname,plant_type,endemic,iucn_category,source) VALUES ("$$1","q$$2q","q$$3q","q$$4q","q$$5q","q$$6q","$$7","$$8","q$$9q","q$$10q");"}' > db_schema/insert_pnamelist.sql
	sed -e 's/'\''/'\'\''/g' ../data/jp_ylist.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_jp_ylist (family,family_cname,cname,name,fullname,plant_type,endemic,iucn_category,source) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","$$6","$$7","q$$8q","q$$9q");"}' > db_schema/insert_jp_ylist.sql
	sed -e 's/'\''/'\'\''/g' ../data/twbirdlist_2014.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_bnamelist (family,family_cname,cname,name,endemic,consv_status) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","q$$6q");"}' > db_schema/insert_bnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/pnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/bnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/insert_pnamelist_pg.sql
	sqlite3 db/twnamelist.db < db_schema/insert_twredlist2017.sql
	sqlite3 db/twnamelist.db < db_schema/insert_pnamelist_pg_synonym.sql
	sqlite3 db/twnamelist.db < db_schema/insert_pnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/insert_jp_ylist.sql
	sqlite3 db/twnamelist.db < db_schema/insert_bnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/update_jp_ylist.sql

clean:
	rm -fr build dist ui_main.py ui_about.py iconResources_rc.py
