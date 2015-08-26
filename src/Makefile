PYUIC=pyuic5
PYTHON=python3

all:
	$(PYUIC) ui/namegen.ui -o ui_window.py

binary:
	pyinstaller -w NGenerator.spec
	./symlink_macos.sh && cp -rf dist/NGenerator.app /Applications/; cp -rf dist/NGenerator.app ../../packages/

update_db:
	# export pgsql view to csv files 
	./exp_twnamelist_view.sh
	sed -e 's/'\''/'\'\''/g' ../data/twnamelist_apg3.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_pnamelist_apg3 (family,family_zh,zh_name,name,fullname,plant_type,endemic,iucn_category,source) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","$$6","$$7","q$$8q","q$$9q");"}' > db_schema/insert_pnamelist_apg3.sql
	sed -e 's/'\''/'\'\''/g' ../data/twnamelist.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_pnamelist (family,family_zh,zh_name,name,fullname,plant_type,endemic,iucn_category,source) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","$$6","$$7","q$$8q","q$$9q");"}' > db_schema/insert_pnamelist.sql
	sed -e 's/'\''/'\'\''/g' ../data/twbirdlist_2014.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_bnamelist (family,family_zh,zh_name,name,endemic,consv_status) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","q$$6q");"}' > db_schema/insert_bnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/pnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/bnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/insert_pnamelist_apg3.sql
	sqlite3 db/twnamelist.db < db_schema/insert_pnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/insert_bnamelist.sql

clean:
	rm -fr build dist
