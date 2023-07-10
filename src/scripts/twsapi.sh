#! /usr/bin/env bash

# set -eux

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

unzip_dir="$HOME/software/unZipped/twsapi_${api_version}"

# If the unzip directory exists, remove it.
if [ -d $unzip_dir ]
then
    echo "Removing $unzip_dir"
    rm -rf $unzip_dir
fi

# unzip the files. For example, this will unzip files into
# ~/software/unZipped/twsapi_1022.01 . The directory will be created.
echo "unzipping the files into $unzip_dir"
unzip -q $download_dir/$api_file -d $unzip_dir

echo "building the wheel"
# This will create a file such as
# ~/software/unZipped/twsapi_1022.01/IBJts/source/pythonclient/dist/ibapi-10.22.1-py3-none-any.whl
cd $unzip_dir/IBJts/source/pythonclient
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
