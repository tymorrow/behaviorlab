#!/usr/bin/env bash
set -e

rm -rf ./build
python3 generate.py

make

rm ./build/*/*.c

find build/ -mindepth 1 -type d -exec tar cvf {}.tar {} \;
find build/ -mindepth 1 -type d -exec tar zcvf {}.tar.gz {} \;
