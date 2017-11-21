import unittest
import pep8

# To run the tests
# cd into the project directory
# python -m unittest discover tests
#
# Sample run:
# $python -m unittest discover tests
# ..
# ----------------------------------------------------------------------
# Ran 2 tests in 20.613s
#
# OK


class Pep8ConformanceTestCase(unittest.TestCase):
    '''Test that all code conforms to pep8 standard'''

    def test_pep8_conformance(self):
        self.pep8style = pep8.StyleGuide(show_source=True)
        files = (['add_weeks.py', 'google_finance.py'])
        self.pep8style.check_files(files)
        self.assertEqual(self.pep8style.options.report.total_errors, 0)


if __name__ == '__main__':
    unittest.main()
