#!/usr/bin/env sh

LCONVERT=lconvert
LANG=(zh_TW zh_CN ja_JP ko_KR)
for (( i=0; i<=3; i++ ))
do
    pylupdate6 mainWindow.py -ts i18n/${LANG[${i}]}/ui_mainWindow_${LANG[${i}]}.ts
    pylupdate6 genlist_api.py -ts i18n/${LANG[${i}]}/genlist_api_${LANG[${i}]}.ts
    pylupdate6 ui_about.py -ts i18n/${LANG[${i}]}/ui_about_${LANG[${i}]}.ts
    pylupdate6 ui_main.py -ts i18n/${LANG[${i}]}/ui_main_${LANG[${i}]}.ts
    pylupdate6 ui_compare.py -ts i18n/${LANG[${i}]}/ui_compare_${LANG[${i}]}.ts
    pylupdate6 ui_combine.py -ts i18n/${LANG[${i}]}/ui_combine_${LANG[${i}]}.ts
    pylupdate6 ui_format.py -ts i18n/${LANG[${i}]}/ui_format_${LANG[${i}]}.ts
    pylupdate6 ui_databases.py -ts i18n/${LANG[${i}]}/ui_databases_${LANG[${i}]}.ts
    ${LCONVERT} -i i18n/${LANG[${i}]}/genlist_api_${LANG[${i}]}.ts \
        i18n/${LANG[${i}]}/ui_about_${LANG[${i}]}.ts \
        i18n/${LANG[${i}]}/ui_mainWindow_${LANG[${i}]}.ts \
        i18n/${LANG[${i}]}/ui_main_${LANG[${i}]}.ts \
        i18n/${LANG[${i}]}/ui_combine_${LANG[${i}]}.ts \
        i18n/${LANG[${i}]}/ui_compare_${LANG[${i}]}.ts \
        i18n/${LANG[${i}]}/ui_format_${LANG[${i}]}.ts \
        i18n/${LANG[${i}]}/ui_databases_${LANG[${i}]}.ts \
        -o i18n/checklister_${LANG[${i}]}.ts
done
