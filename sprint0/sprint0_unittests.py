'''
Ryan Phillips 
UMKC CS 449 Sprint 0 Unit Tests
Languag: Python
Unit Test Framework: unittest (pythons version of java JUnit)
sprint0_unittests.py
'''

import unittest

'''
I use a basic trial division prime generator that I created for my part of CS 404 prject
to test on.
'''

import time
from math import sqrt

'''
Trial Division Prime Check

This is good for one off checks because it wont allocate any memory.
However, when generating primes dont use this check. It will be slower because of the absent use of a prevuious found primes cache.

trial_division_generator() below uses a previous found prime cache and prime gap to genrate much faster checks

Time Complexity = O(sqrt(N))
Space Complexity = O(1)
'''
def trial_division_check(number):
	# Passed invalid argument
	if not isinstance(number, (int, float)):
		return False
		
	# Number passed is non positive
	if number <= 0:
		return False
	
	# one is a special case and is not prime because has only one factor
	if number == 1:
		return False
	
	# sqrt of number is hard constraint for primality factorization
	square_root = int(sqrt(number))

	# Check for any valid factors starting from 2 going to square root (Inclusive)
	# Iff a valid factor is found then the number is not prime
	# linear time complexity
	for denominator in range(2, square_root + 1): # -> O(sqrt(N))
		if (number % denominator) == 0:
			return False # Factor found -> Not Prime

	# No factors found or square root was less than or equal to 1 -> Is Prime
	return True


'''
Units tests for prime generator
'''
class TestPrimeGeneratorFunction(unittest.TestCase):
    def test_single_prime(self):
        self.assertEqual(trial_division_check(7), True)
    def test_multiple_primes(self):
      self.assertEqual([trial_division_check(3), trial_division_check(7), trial_division_check(6)], [True, True, False])

if __name__ == '__main__':
    unittest.main()