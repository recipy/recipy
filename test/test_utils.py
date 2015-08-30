import unittest

from recipyCommon import utils

class TestMultipleInsert(unittest.TestCase):

	def test_blank_list(self):
		# Blank list to start with
		l = []
		utils.multiple_insert(l, [1, 2, 3])

		self.assertSequenceEqual(l,
								 [3, 2, 1])

	def test_blank_addition(self):
		# Blank list to start with
		l = [1, 2, 3]
		utils.multiple_insert(l, [])

		self.assertSequenceEqual(l,
								 [1, 2, 3])

	def test_standard_usage(self):
		# Standard usage
		l = ['a', 'b', 'c']
		utils.multiple_insert(l, ['second', 'first'])

		self.assertSequenceEqual(l,
								 ['first', 'second', 'a', 'b', 'c'])

