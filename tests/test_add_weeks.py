
import unittest
import os
import subprocess
import pandas as pd

# To run the tests
# cd into the project directory
# python3 -m unittest discover tests
#
# Sample run:
# $python3 -m unittest discover tests
# .
# ----------------------------------------------------------------------
# Ran 1 test in 0.005s
#
# OK


class functionalTestCase(unittest.TestCase):
    '''Test if the script is ok functionally or not'''

    def test_functional(self):
        fname = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'test_defs.json')
        test_defs = pd.read_json(fname)
        for row in test_defs.itertuples():
            print('testing: ', row.cmd)
            # import time
            # start = time.time()
            obtained = subprocess.check_output(row.cmd,
                                               universal_newlines=True)
            # print("time taken = ", time.time()-start)
            with open(row.out_file, 'r') as fh:
                expected = fh.read()
                self.assertEqual(obtained, expected, row.tag)


if __name__ == '__main__':
    unittest.main()
