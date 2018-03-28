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


class Pep8ConformanceTestCase(unittest.TestCase):
    '''Test that all code conforms to pep8 standard'''

    def test_pep8_conformance(self):
        pep8style = StyleGuide(show_source=True)
        # files = (['add_weeks.py', 'google_finance.py'])
        from list_files import list_python_files
        files = list_python_files('.')
        print('Checking', files, 'for pep8 conformance.')
        pep8style.check_files(files)
        self.assertEqual(pep8style.options.report.total_errors, 0)


if __name__ == '__main__':
    unittest.main()
