PYUIC=pyuic5
PYRCC=pyrcc5
PYTHON=python3

all:
	#$(PYUIC) ui/main_window.ui -o ui_window.py
	cp ui/ui_main2.ui ui/ui_main.ui
	$(PYUIC) ui/ui_main.ui -o ui_main.py
	$(PYRCC) -o iconResources_rc.py iconResources.qrc

translate:
	pylupdate5 window.py -ts i18n/window_zh_TW.ts
	pylupdate5 window.py -ts i18n/window_zh_CN.ts
	pylupdate5 window.py -ts i18n/window_ja_JP.ts
	pylupdate5 window.py -ts i18n/window_ko_KR.ts
	pylupdate5 ui_window.py -ts i18n/ui_window_zh_TW.ts
	pylupdate5 ui_window.py -ts i18n/ui_window_zh_CN.ts
	pylupdate5 ui_window.py -ts i18n/ui_window_ja_JP.ts
	pylupdate5 ui_window.py -ts i18n/ui_window_ko_KR.ts
	pylupdate5 ui_main.py -ts i18n/ui_window_zh_TW.ts
	pylupdate5 ui_main.py -ts i18n/ui_window_zh_CN.ts
	pylupdate5 ui_main.py -ts i18n/ui_window_ja_JP.ts
	pylupdate5 ui_main.py -ts i18n/ui_window_ko_KR.ts

binary:
	pyinstaller --onefile checklister.spec
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
	rm -fr build dist
