#! /usr/bin/env bash

# This script will
# * build a wheel for the TWS python api
# * copy the wheel file into a local repo directory
# * remove the files created during the build process
#
# tags | IBKR

set -eu

# sample url: 'https://interactivebrokers.github.io/downloads/twsapi_macunix.1022.01.zip'
api_version='1022.01'
api_file="twsapi_macunix.${api_version}.zip"
url="https://interactivebrokers.github.io/downloads/${api_file}"

download_dir="$HOME/software/zipped/twsapi"
mkdir -p $download_dir
# man page of wget: https://linux.die.net/man/1/wget
# -nc | --no-clobber
#   Do not clobber, or overwrite the file upon repeated download
# -P | --directory-prefix
#   Download the file to this directory
wget $url -nc -P $download_dir

build_root="$HOME/software/compileHere"
mkdir -p build_root

build_dir="$build_root/twsapi_${api_version}"
# Remove files created during prior builds
if [ -d $build_dir ]
then
    echo "Removing $build_dir"
    rm -rf $build_dir
fi

# unzip the files. For example, this will unzip files into
# ~/software/compileHere/twsapi_1022.01 . The directory will be created as part
# of unzip.
echo "unzipping the files into $build_dir"
unzip -q $download_dir/$api_file -d $build_dir

echo "building the wheel"
# This will create a file such as
# ~/software/unZipped/twsapi_1022.01/IBJts/source/pythonclient/dist/ibapi-10.22.1-py3-none-any.whl
cd $build_dir/IBJts/source/pythonclient
python3 setup.py bdist_wheel

# To install the wheel
#   % conda activate market_data_processor
#   % python -m pip install --user --upgrade ~/software/unZipped/twsapi_1022.01/IBJts/source/pythonclient/dist/ibapi-10.22.1-py3-none-any.whl
#
# To test it
#   % python
#   Python 3.11.3 (main, May 15 2023, 15:45:52) [GCC 11.2.0] on linux
#   >>> import ibapi
#
# To remove ibapi
#   % python -m pip uninstall ibapi

# Copy the wheel into the local repo directory
local_repo_dir="$HOME/software/dist"
mkdir -p $local_repo_dir
wheel_version=`python3 -c "from ibapi import get_version_string; version=get_version_string(); print(version)"`
wheel_file=ibapi-${wheel_version}-py3-none-any.whl
cp -v dist/$wheel_file $local_repo_dir

# Remove files created during build
if [ -d $build_dir ]
then
    echo "Removing $build_dir"
    rm -rf $build_dir
fi
