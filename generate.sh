rm -rf ./build

python generate.py

make

rm ./build/*/*.c

find build/ -mindepth 1 -type d -exec tar cvf {}.tar {} \;
find build/ -mindepth 1 -type d -exec tar zcvf {}.tar.gz {} \;
