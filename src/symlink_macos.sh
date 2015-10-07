#!/usr/bin/env bash
if [ `uname` == "Darwin" ]; then
    cd dist/NGenerator.app/Contents/MacOS
    unlink db; unlink include; unlink lib
    unlink i18n; #unlink qt_menu.nib
    #unlink bin; unlink share; unlink changelog
    ln -s ../Resources/db
    ln -s ../Resources/include
    ln -s ../Resources/lib
    ln -s ../Resources/i18n
    #ln -s ../Resources/qt_menu.nib
    #ln -s ../Resources/share
    #ln -s ../Resources/bin
    #ln -s ../Resources/pandoc
else
    echo "pass"
fi

