#!/usr/bin/env bash
if [ `uname` == "Darwin" ]; then
    cd dist/NGenerator.app/Contents/MacOS
    unlink db; unlink include; unlink lib
    ln -s ../Resources/db
    ln -s ../Resources/include
    ln -s ../Resources/lib
else
    echo "pass"
fi

