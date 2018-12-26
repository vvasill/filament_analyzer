#!/usr/bin/env python3
#unittests.py

from __future__ import print_function, division, unicode_literals

import unittest
import numpy as np
import filamentyzer

class NameTestCase(unittest.TestCase):
	def test(self):
		name = 'filamentyzer'
		self.assertEqual(filamentyzer.name, name, msg='name should be {}'.format(name))

class IsFilamentyzerTestCase(unittest.TestCase):
	def test_first(self):
		data = np.zeros((2,2))
		self.assertTrue(plot_heat_map("infile", data), msg='plot_heat_map is ok')


# This function can be used in `setup.py` as `test_suite` keyword argument
def test_suite():
	suite = unittest.defaultTestLoader.loadTestsFromName(__name__)
	return suite

if __name__ == '__main__':  # checks if this file executed as script
	unittest.main()

