# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/env python3

# <codecell>

import csv
import sqlite3
import sys
import subprocess

def fmtname(name):
    n_split = name.split(' ')
    lenf = len(n_split)
    if 'var.' in n_split:
        sub_idx = n_split.index('var.')
        fmt_name = '*' + " ".join(str(item) for item in n_split[0:2])+ '*'
        fmt_author = " ".join(str(item) for item in n_split[sub_idx+2:lenf])
        fmt_sub = '*' + str(n_split[sub_idx+1]) + '* '
        fmt_oname = fmt_name + ' var. ' + fmt_sub + fmt_author
    elif 'subsp.' in n_split:
        sub_idx = n_split.index('subsp.')
        fmt_name = '*' + " ".join(str(item) for item in n_split[0:2])+ '*'
        fmt_author = " ".join(str(item) for item in n_split[sub_idx+2:lenf])
        fmt_sub = '*' + str(n_split[sub_idx+1]) + '* '
        fmt_oname = fmt_name + ' subsp. ' + fmt_sub + fmt_author
    elif 'fo.' in n_split:
        sub_idx = n_split.index('fo.')
        fmt_name = '*' + " ".join(str(item) for item in n_split[0:2])+ '*'
        fmt_author = " ".join(str(item) for item in n_split[sub_idx+2:lenf])
        fmt_sub = '*' + str(n_split[sub_idx+1]) + '* '
        fmt_oname = fmt_name + ' fo. ' + fmt_sub + fmt_author
    elif '×' in n_split:
        fmt_name = '*' + " ".join(str(item) for item in n_split[0:3])+ '*'
        fmt_author = " ".join(str(item) for item in n_split[3:lenf])
        fmt_oname = fmt_name + ' ' + fmt_author
    else:
        fmt_name = '*' + " ".join(str(item) for item in n_split[0:2])+ '*'
        fmt_author = " ".join(str(item) for item in n_split[2:lenf])
        fmt_oname = fmt_name + ' ' + fmt_author
    return(fmt_oname)

def convert(oformat='docx'):
    subprocess.call(['pandoc', 'output.md', '-o', 'output.'+oformat])
    
def main(oformat):
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
      plant_type integer
    );
    '''
    sample_create = '''
    CREATE TABLE sample (
      zh_name varchar
    );
    '''
    curs.execute(blist_create)
    curs.execute(sample_create)
    with open(sys.argv[1], newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            insert_db = '''
            INSERT INTO namelist (family,family_zh,zh_name,name,fullname,plant_type)
            VALUES ("%s", "%s", "%s", "%s", "%s", %s);
            ''' % (row[0], row[1], row[2], row[3], row[4], row[5])
            curs.execute(insert_db)
            conn.commit()
    with open(sys.argv[2], newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            insert_db = '''
            INSERT INTO sample (zh_name) VALUES ("%s");
            ''' % row[0]
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
    pt_name = ('蕨類植物 Ferns and Fern Allies', '裸子植物 Gymnosperms', "雙子葉植物 'Dicotyledons'", '單子葉植物 Monocotyledons')
    for i in range(0,4):
        pt_sql = '''INSERT INTO plant_type (plant_type, pt_name) 
        VALUES (%i, "%s");''' % (plant_type[i], pt_name[i])
        curs.execute(pt_sql)
        conn.commit()
    
    with open('output.md', 'w+') as f:
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
        curs.execute(count_family)
        family_no = curs.fetchall()[0][0]
        curs.execute(count_species)
        species_no = curs.fetchall()[0][0]
        f.write('名錄中共有 {} 科、{} 種'.format(family_no, species_no))
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
            f.write('\n##'+pt_plant_type[i][1]+'\n\n')
            pt_family_sql = '''
            select distinct family,family_zh from sample s left outer join namelist n 
            on s.zh_name=n.zh_name where n.plant_type=%i
            order by plant_type,family;
            ''' % pt_plant_type[i][0]
            curs.execute(pt_family_sql)
            pt_family = curs.fetchall()
            for j in range(0,len(pt_family)):   
                fam = str(m) + '. **' + pt_family[j][0]
                fam_zh = pt_family[j][1]+'**'
                f.write('\n')
                f.write(fam+' '+fam_zh+'\n')
                pt_family_sp = '''
                    select distinct fullname,n.zh_name from sample s left outer join namelist n 
                    on s.zh_name=n.zh_name where n.plant_type=%i and family='%s'
                    order by plant_type,family,fullname;
                ''' % (pt_plant_type[i][0], pt_family[j][0])
                curs.execute(pt_family_sp)
                pt_family_sp = curs.fetchall()
                m = m + 1
                for k in range(0,len(pt_family_sp)):
                    f.write('    ' + str(n) + '. ' + fmtname(pt_family_sp[k][0]) + ' ' + pt_family_sp[k][1] +'\n')
                    n = n + 1
        f.close()        
        convert(oformat)
if __name__=='__main__':
    main(oformat='docx')

# <codecell>


