import unittest
try:
    from pycodestyle import StyleGuide
except ImportError:
    from pep8 import StyleGuide


# To run the tests
# cd into the project directory
# python3 -m unittest discover tests
#
# Sample run:
# $python3 -m unittest discover tests
# ..
# ----------------------------------------------------------------------
# Ran 2 tests in 20.613s
#
# OK

# Note:- If you are copy pasting code from here, see rutils/python3/tests/test_codestyle.py first.
# Common between the two:
# * Both use pycodestyle
# Enhancements in rutils/python3/tests/test_codestyle.py
# * uses pytest instead of unittest
# * uses configuration file to ignore errors such as E501.

class Pep8ConformanceTestCase(unittest.TestCase):
    '''Test that all code conforms to pep8 standard'''

    def test_pep8_conformance(self):
        # Ignore the following errors:
        # E501 line too long (xxx > 79 characters)
        pep8style = StyleGuide(show_source=True, ignore=['E501'])
        # files = (['add_weeks.py', 'google_finance.py'])
        from list_files import list_python_files
        files = list_python_files('.')
        print('Checking', files, 'for pep8 conformance.')
        report = pep8style.check_files(files)
        report.print_statistics()
        self.assertEqual(pep8style.options.report.total_errors, 0)


if __name__ == '__main__':
    unittest.main()
