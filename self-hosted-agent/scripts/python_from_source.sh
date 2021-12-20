#!/bin/bash

VERSION=$1

echo "[*] Installing Python $VERSION";

source $HELPER_SCRIPTS/document.sh

PYTHONFOLDER=$AGENT_TOOLSDIRECTORY/Python/$VERSION/x64

cd /tmp/
wget https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tar.xz
tar -xf Python-$VERSION.tar.xz
cd Python-$VERSION
./configure --prefix=$PYTHONFOLDER

make -j`nproc`
make altinstall
touch $AGENT_TOOLSDIRECTORY/Python/$VERSION/x64.complete

cd ..
rm Python-$VERSION.tar.xz
rm -rf Python-$VERSION

# create symlinks
cd $AGENT_TOOLSDIRECTORY/Python/$VERSION/x64/bin
export PATH=$(pwd):$PATH
ln -s $(find -name 'python*' ! -name '*config' ! -name '*m') python
ln -s pip* pip

cd /
ln -s  $AGENT_TOOLSDIRECTORY/Python/$VERSION/x64/bin/python /usr/bin/python
ln -s  $AGENT_TOOLSDIRECTORY/Python/$VERSION/x64/bin/pip  /usr/local/bin/pip
pip install --upgrade pip
pip install -r /requirements.txt