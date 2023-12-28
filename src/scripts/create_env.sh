#! /usr/bin/env bash
# set -eux
script_dir="$(dirname "$(readlink -f "$0")")"
project_dir=$(dirname $(dirname $script_dir))
env_dir=$project_dir/envs
env_file_name=env_market_data_processor.yml
env_file_path=$env_dir/$env_file_name
env_name=market_data_processor

# Show the creation time of the current  environment
conda env list | grep -v '^#' | grep $env_name | perl -lane 'print $F[-1]' | xargs ls -lrt1d

conda env remove --name $env_name
conda env create -f $env_file_path

# Show the creation time of the new environment
conda env list | grep -v '^#' | grep $env_name | perl -lane 'print $F[-1]' | xargs ls -lrt1d
