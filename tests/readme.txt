-------------------------------------------------------------------------------
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
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
If the tests in tests/test_codestyle.py are failing, try running black on the
source code files

Sample command:
black --skip-string-normalization your_file.py
or more simply
black -S your_file.py

where the --skip-string-normalization tells Black not to convert single
quotes to double quotes.

Note: There are two ways to use the --skip-string-normalization flag. You can
either add it to the black command as above or add the following lines to
pyproject.toml

[tool.black]
skip-string-normalization = true

and then just run black without any options.

black your_file.py
-------------------------------------------------------------------------------
