#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import sqlite3
import sys
import subprocess
import codecs
import re

# format the typesetting of names
class genlist(object):
    def __init__(self):
        pass
#    def __init__(self, name, dbfile, inputfile, oformat, ofile_prefix):
#        self.name = name
#        self.dbfile = dbfile
#        self.inputfile = inputfile
#        self.oformat = oformat
#        self.ofile_prefix = ofile_prefix


    def fmtname(self, name):
        n_split = name.split(' ')
        lenf = len(n_split)
        # typesetting
        italic_b = '*'
        italic_e = '*'
        if 'var.' in n_split:
            sub_idx = n_split.index('var.')
            fmt_name = italic_b + " ".join(str(item) for item in n_split[0:2])+ italic_e
            fmt_author = " ".join(str(item) for item in n_split[sub_idx+2:lenf])
            fmt_sub = italic_b + str(n_split[sub_idx+1]) + italic_e
            fmt_oname = fmt_name + ' var. ' + fmt_sub + ' ' + fmt_author
        elif 'subsp.' in n_split:
            sub_idx = n_split.index('subsp.')
            fmt_name = italic_b + " ".join(str(item) for item in n_split[0:2])+ italic_e
            fmt_author = " ".join(str(item) for item in n_split[sub_idx+2:lenf])
            fmt_sub = italic_b + str(n_split[sub_idx+1]) + italic_e
            fmt_oname = fmt_name + ' subsp. ' + fmt_sub + ' ' + fmt_author
        elif 'fo.' in n_split:
            sub_idx = n_split.index('fo.')
            fmt_name = italic_b + " ".join(str(item) for item in n_split[0:2])+ italic_e
            fmt_author = " ".join(str(item) for item in n_split[sub_idx+2:lenf])
            fmt_sub = italic_b + str(n_split[sub_idx+1]) + italic_e
            fmt_oname = fmt_name + ' fo. ' + fmt_sub + ' ' + fmt_author
        elif '×' in n_split:
            fmt_name = italic_b + " ".join(str(item) for item in n_split[0:3])+ italic_e
            fmt_author = " ".join(str(item) for item in n_split[3:lenf])
            fmt_oname = fmt_name + ' ' + fmt_author
        else:
            fmt_name = italic_b + " ".join(str(item) for item in n_split[0:2])+ italic_e
            fmt_author = " ".join(str(item) for item in n_split[2:lenf])
            fmt_oname = fmt_name + ' ' + fmt_author
        # 作者中訂正(ex)需使用斜體
        fmt_oname = re.sub(' ex ', ' ' + italic_b + 'ex' + italic_e + ' ', fmt_oname)
        return(fmt_oname)

    # convert markdown to other fileformats using pandoc
    def convert(self, oformat='docx', ofile_prefix='output'):
        subprocess.call(['pandoc', ofile_prefix+'.md', '-o', ofile_prefix+'.'+oformat])
        
    def generator(self, dbfile, inputfile, oformat='docx', ofile_prefix='output'):
        """
        dbfile
        inputfile
        oformat 
        ofile_prefix
        """
        conn = sqlite3.connect(':memory:')
        curs = conn.cursor()
        # default db table
        # family|family_zh|zh_name|name|fullname|plant_type(1='Ferns',2='Gymnosperms',3='Dicots',4=Monocots)
        # Vittariaceae|書帶蕨科|車前蕨|Antrophyum obovatum|Antrophyum obovatum Bak.|1
        blist_create = '''
        CREATE TABLE namelist (
          family varchar,
          family_zh varchar,
          zh_name varchar,
          name varchar,
          fullname varchar,
          plant_type integer,
          endemic integer,
          iucn_category varchar,
          source varchar
        );
        '''
        sample_create = '''
        CREATE TABLE sample (
          zh_name varchar
        );
        '''
        curs.execute(blist_create)
        curs.execute(sample_create)
        with open(dbfile, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                insert_db = '''
                INSERT INTO namelist (
                    family,
                    family_zh,
                    zh_name,
                    name,
                    fullname,
                    plant_type,
                    endemic,
                    iucn_category,
                    source)
                VALUES ("%s", "%s", "%s", "%s", "%s", %s,  %s, "%s", "%s");
                ''' % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                curs.execute(insert_db)
                conn.commit()
        with open(inputfile, newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                # substitute 台 to 臺
                zhname = re.sub('台([灣|北|中|西|南|東])',r'臺\1', row[0])
                insert_db = '''
                INSERT INTO sample (zh_name) VALUES ("%s");
                ''' % zhname
                curs.execute(insert_db)
                conn.commit()
        # insert plant_type
        curs.execute('DROP TABLE IF EXISTS plant_type;')
        plant_type_table = '''
        CREATE TABLE plant_type (
            plant_type integer,
            pt_name varchar
        );
        '''
        curs.execute(plant_type_table)
        plant_type = (1, 2, 3, 4)
        pt_name = ('蕨類植物 Ferns and Lycophytes', '裸子植物 Gymnosperms', "雙子葉植物 'Dicotyledons'", '單子葉植物 Monocotyledons')
        for i in range(0,4):
            pt_sql = '''INSERT INTO plant_type (plant_type, pt_name) 
            VALUES (%i, "%s");''' % (plant_type[i], pt_name[i])
            curs.execute(pt_sql)
            conn.commit()
        
        with codecs.open(ofile_prefix +'.md', 'w+', 'utf-8') as f:
            f.write('# 維管束植物名錄')
            f.write('\n')
            count_family = '''
            SELECT count(*) from (SELECT distinct family from sample s left outer join namelist n 
                    on s.zh_name=n.zh_name) as f;
            '''
            count_species = '''
            SELECT count(*) from (SELECT distinct n.zh_name from sample s left outer join namelist n 
                    on s.zh_name=n.zh_name) as f;
            '''
            not_exist_sp = '''
            SELECT distinct s.zh_name from sample s left outer join namelist n 
                    on s.zh_name=n.zh_name where n.zh_name is null;
            '''
            curs.execute(count_family)
            family_no = curs.fetchall()[0][0]
            curs.execute(count_species)
            species_no = curs.fetchall()[0][0]
            curs.execute(not_exist_sp)
            no_sp = curs.fetchall()
            nsp = []
            for i in no_sp:
                nsp.append(i[0])
            nsp = ', '.join(nsp)
            if len(nsp) > 0:
                f.write('\n')
                f.write('<font color="red">輸入名錄中，下列物種不存在於物種資料庫中：{} ，請再次確認物種中名是否和資料庫中相同</font>\n'.format(nsp))
            f.write('\n')
            f.write('本名錄中共有 {} 科、{} 種，科名後括弧內為該科之物種總數。'.format(family_no, species_no))
            f.write('"#" 代表特有種，"*" 代表歸化種，"†" 代表栽培種。')
            f.write('中名後面括號內的縮寫代表依照「臺灣維管束植物初評名錄」中依照 IUCN 瀕危物種所評估等級，')
            f.write('EX: 滅絕, EW: 野外滅絕, RE: 區域性滅絕, CR: 嚴重瀕臨滅絕, ')
            f.write('EN: 瀕臨滅絕, VU: 易受害, NT: 接近威脅, DD: 資料不足。若未註記者代表安全(Least concern)')
            f.write('\n')
            pt_plant_type_sql = '''
                SELECT p.plant_type,p.pt_name
                FROM plant_type p,
                    (SELECT distinct plant_type from sample s left outer join namelist n 
                    on s.zh_name=n.zh_name order by plant_type) as t
                WHERE p.plant_type = t.plant_type;
            '''
            curs.execute(pt_plant_type_sql)
            pt_plant_type = curs.fetchall()
            n = 1
            m = 1
            for i in range(0,len(pt_plant_type)):
                f.write('\n')
                f.write('\n###'+pt_plant_type[i][1]+'\n\n')
                pt_family_sql = '''
                select distinct family,family_zh from sample s left outer join namelist n 
                on s.zh_name=n.zh_name where n.plant_type=%i
                order by plant_type,family;
                ''' % pt_plant_type[i][0]
                curs.execute(pt_family_sql)
                pt_family = curs.fetchall()
                for j in range(0,len(pt_family)):
                    sp_number_in_fam = '''
                        select count(*) from 
                        (select distinct fullname,n.zh_name from sample s left outer join namelist n 
                        on s.zh_name=n.zh_name where n.plant_type=%i and family='%s'
                        order by plant_type,family,fullname) as a;
                    ''' % (pt_plant_type[i][0], pt_family[j][0])
                    curs.execute(sp_number_in_fam)
                    fam_spno = curs.fetchall()[0][0]
                    fam = str(m) + '. **' + pt_family[j][0]
                    fam_zh = pt_family[j][1]+'**'
                    f.write('\n')
                    f.write(fam+' '+fam_zh+' (%i)\n' % fam_spno)
                    pt_family_sp = '''
                        select distinct fullname,n.zh_name,n.endemic,n.source,n.iucn_category from sample s left outer join namelist n 
                        on s.zh_name=n.zh_name where n.plant_type=%i and family='%s'
                        order by plant_type,family,fullname;
                    ''' % (pt_plant_type[i][0], pt_family[j][0])
                    curs.execute(pt_family_sp)
                    pt_family_sp = curs.fetchall()
                    m = m + 1
                    # output species within a family
                    for k in range(0,len(pt_family_sp)):
                        # check the endmic species
                        if pt_family_sp[k][2]==1:
                            ENDEMIC = "#"
                        else:
                            ENDEMIC = ''
                        # check the source 
                        if pt_family_sp[k][3]=='栽培':
                            SRC = '†'
                        elif pt_family_sp[k][3]=='歸化':
                            SRC = '*'
                        else:
                            SRC = ''
                        # IUCN category
                        if len(pt_family_sp[k][4]) == 2:
                            IUCNCAT = ' (%s)' % pt_family_sp[k][4]
                        else:
                            IUCNCAT = ''
                        spinfo = ' ' + ENDEMIC + SRC + IUCNCAT
                        if spinfo is not None:
                            f.write('    ' + str(n) + '. ' + self.fmtname(pt_family_sp[k][0]) + ' ' + pt_family_sp[k][1] + spinfo + '\n')
                        else:
                            f.write('    ' + str(n) + '. ' + self.fmtname(pt_family_sp[k][0]) + ' ' + pt_family_sp[k][1] +'\n')
                        n = n + 1
            f.close()        
            self.convert(oformat, ofile_prefix)
