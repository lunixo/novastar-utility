#!/bin/bash

CMD_FILENAME=/usr/bin/novastar;
APP_DIR="$( dirname -- "${BASH_SOURCE[0]}"; )";
APP_DIR="$( realpath -e -- "$APP_DIR"; )";

cd $APP_DIR

cp -rf novastar $CMD_FILENAME
sed -i 's|\${APP_DIR}|'${APP_DIR}'|g' $CMD_FILENAME
chmod +x $CMD_FILENAME