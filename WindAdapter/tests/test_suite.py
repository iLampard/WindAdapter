# -*- coding: utf-8 -*-

import os
import sys
import unittest
thisFilePath = os.path.abspath(__file__)
sys.path.append(os.path.sep.join(thisFilePath.split(os.path.sep)[:-3]))
from WindAdapter.tests.test_api import TestApi


def test():
    print('Python ' + sys.version)
    suite = unittest.TestSuite()
    tests = unittest.TestLoader().loadTestsFromTestCase(TestApi)
    suite.addTests(tests)

    res = unittest.TextTestRunner(verbosity=3).run(suite)
    if len(res.errors) >= 1 or len(res.failures) >= 1:
        sys.exit(-1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    test()
