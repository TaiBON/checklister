PYUIC=pyuic5
PYRCC=pyrcc5
PYTHON=python3

all: mui translate binary

mui:
	$(PYUIC) ui/ui_main.ui -o ui_main.py
	$(PYUIC) ui/ui_about.ui -o ui_about.py
	$(PYRCC) -o iconResources_rc.py iconResources.qrc

translate:
	./make_trans_ui.sh

binary:
	pyinstaller --onefile --windowed checklister.spec
	rm -fr /Applications/checklister.app
	./symlink_macos.sh && cp -rf dist/checklister.app /Applications/; cp -rf dist/checklister.app ../../packages/

create_db_schema:
	rm db/twnamelist.db
	sqlite3 db/twnamelist.db < db_schema/pnamelist.sql

update_db:

	# export pgsql view to csv files
	./exp_twnamelist_view.sh
	sed -e 's/'\''/'\'\''/g' ../data/twnamelist_pg.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_pnamelist_pg (family,family_cname,cname,name,fullname,plant_type,endemic,iucn_category,source) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","$$6","$$7","q$$8q","q$$9q");"}' > db_schema/insert_pnamelist_pg.sql
	sed -e 's/'\''/'\'\''/g' ../data/twnamelist.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_pnamelist (family,family_cname,cname,name,fullname,plant_type,endemic,iucn_category,source) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","$$6","$$7","q$$8q","q$$9q");"}' > db_schema/insert_pnamelist.sql
	sed -e 's/'\''/'\'\''/g' ../data/jp_ylist.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_jp_ylist (family,family_cname,cname,name,fullname,plant_type,endemic,iucn_category,source) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","$$6","$$7","q$$8q","q$$9q");"}' > db_schema/insert_jp_ylist.sql
	sed -e 's/'\''/'\'\''/g' ../data/twbirdlist_2014.csv | awk -v q="'" -F'|' '{print "INSERT INTO dao_bnamelist (family,family_cname,cname,name,endemic,consv_status) VALUES ("q$$1q","q$$2q","q$$3q","q$$4q","q$$5q","q$$6q");"}' > db_schema/insert_bnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/pnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/bnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/insert_pnamelist_pg.sql
	sqlite3 db/twnamelist.db < db_schema/insert_pnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/insert_jp_ylist.sql
	sqlite3 db/twnamelist.db < db_schema/insert_bnamelist.sql
	sqlite3 db/twnamelist.db < db_schema/update_jp_ylist.sql

clean:
	rm -fr build dist ui_main.py ui_about.py iconResources_rc.py
