#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import genlist_api

if __name__=='__main__':
    if len(sys.argv) < 8:
        print("Usage:")
        print("    -h print this help")
        print("    -d database file (sqlite.db), ex: twnamelist.db")
        print("    -t taxa; 1: vascular plants (APGIII), 2: Flora of Taiwan 2nd Edi.")
        print("       3: Birdlist of Taiwan")
        print("    -s input species file (csv or txt, chinese common names)")
        print("    -f export file format, default: markdown (md) and docx")
        print("       optional: all pandoc supported fileformats")
        print("    -o please specify the prefix of output filename (default is output)")
        sys.exit()
    else:
        for i in range(0,len(sys.argv)):
            if sys.argv[i] == '-f':
                argv_f = sys.argv[i+1]
            elif sys.argv[i] == '-o':
                argv_fpre = sys.argv[i+1] 
            elif sys.argv[i] == '-d':
                argv_db = sys.argv[i+1]
            elif sys.argv[i] == '-t':
                tab_list = sys.argv[i+1]
                if int(tab_list) < 0 or int(tab_list) > 4:
                    print("table out of index, use Flora of Taiwan APGIII")
                    argv_tab = 'dao_pnamelist_apg3'
                elif int(tab_list) == 1:
                    argv_tab = 'dao_pnamelist_apg3'
                elif int(tab_list) == 2:
                    argv_tab = 'dao_pnamelist'
                elif int(tab_list) == 3:
                    argv_tab = 'dao_bnamelist'
                else:
                    argv_tab = 'dao_pnamelist_apg3'
            elif sys.argv[i] == '-s':
                argv_sp = sys.argv[i+1]
        if argv_f is None:
            argv_f = 'docx'
        if argv_fpre is None:
            argv_fpre = 'output'
        try:
            g = genlist_api.Genlist()
            g.genEngine(dbtable=argv_tab, inputfile=argv_sp, dbfile=argv_db, oformat=argv_f, ofile_prefix=argv_fpre)
        except BaseException as e:
            print(e)
# <codecell>
