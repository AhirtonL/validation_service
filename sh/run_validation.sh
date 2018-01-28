#!/bin/bash

HOME=$(pwd)
cd "$( cd -P -- "$(dirname -- "$(command -v -- "$0")")" && pwd -P )/.."
BASE=$(pwd)

cd ${BASE}/python
python validation_driver.py $@

cd $HOME

