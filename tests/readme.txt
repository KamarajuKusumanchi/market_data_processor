To run the tests

cd ~/work/github/market_data_processor
conda activate market_data_processor
# Ignore the tests in the directory named 'deprecated'
pytest -p no:faulthandler --ignore=deprecated
  or
python -m pytest -p no:faulthandler --ignore=deprecated

See also:
* https://stackoverflow.com/questions/11117062/how-to-tell-py-test-to-skip-certain-directories
  - shows how to skip certain directories when running pytest. Here I am using
  the command line option. But you can also do it using pytest.ini config file.
