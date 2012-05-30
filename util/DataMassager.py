import re

class DataMassager(object):
	r"""
	Provides a series of static methods to strip (removing expected
	user-entered characters from), check (validate), clean (strip and check
	at once), and format various common data formats.

	@author Richard Laager \<rlaager\@wiktel.com\>
	"""

	__allNumbers = re.compile(r'^\d+$')

	# NOTE: Update the documentation for the stripPhone method when
	#       changing the regular expression defined below.
	__stripPhone = re.compile(r'[.() +-]')

	def __new__(cls, *args, **kwds):
		r"""
		Placeholder constructor.

		This class contains only static methods. It should not be
		instantiated.

		@exception NotImplementedError This exception is always thrown
		by this method. This is to indicate that this method should not
		be used. Callers must not depend on the specific exception
		being thrown or even that an exception is always thrown.
		"""
		raise NotImplementedError, \
			'This class contains only static methods.'

	def allNumbers(data):
		r"""
		Checks if the supplied @a data is all numbers.

		This method checks the supplied @a data to see if it consists
		of all numbers.

		@param data A string (or something that can be converted to a
		            string using the str() built-in) of data.

		@return     A boolean value indicating if the supplied @a data
		            is all numbers.

		@code
		>>> DataMassager.allNumbers('0')
		1

		@endcode

		@code
		>>> DataMassager.allNumbers('13049238432402398423')
		1

		@endcode

		@code
		# This example shows that since this is a character match, the
		# period (@c .) doesn't count as a decimal point.
		>>> DataMassager.allNumbers('0.0')
		0

		@endcode

		@code
		# This example shows that since this is a character match, the
		# dash (@c -) doesn't count as a negative sign.
		>>> DataMassager.allNumbers('-1')
		0

		@endcode

		@code
		# This example shows that since this is a character match, the
		# plus (@c +) doesn't count as a positive sign.
		>>> DataMassager.allNumbers('+1')
		0

		@endcode
		"""

		if data == None:
			return False

		if DataMassager.__allNumbers.match(str(data)):
			return True
		else:
			return False
	allNumbers = staticmethod(allNumbers)

	# PHONE NUMBER FUNCTIONS #

	def checkPhone(data):
		r"""
		Checks if the supplied @a data is a valid phone number.

		This method checks if the supplied @a data is a valid (North
		American) phone number (after stripping characters using the
		stripPhone() method).

		@param data A string (or something that can be converted to a
		            string using the str() built-in) of data.

		@return     A boolean value indicating if the supplied @a data
		            is a valid phone number

		@code
		>>> DataMassager.checkPhone('8885551212')
		1

		@endcode

		@code
		>>> DataMassager.checkPhone('18885551212')
		1

		@endcode

		@code
		>>> DataMassager.checkPhone('888-555-1212')
		1

		@endcode

		@code
		>>> DataMassager.checkPhone('+1 (888) 555-1212')
		1

		@endcode

		@code
		# This example shows that a phone number doesn't have to look
		# normal as long as only the allowed characters are used and it
		# has the right length after the extra characters are stripped
		# using the stripPhone() method.
		>>> DataMassager.checkPhone('8((()8++--8-5(55-1+++21     2...')
		1

		@endcode

		@code
		# This phone number contains illegal characters.
		>>> DataMassager.checkPhone('#8885551212')
		0

		@endcode

		@code
		# This phone number is too short.
		>>> DataMassager.checkPhone('888555121')
		0

		@endcode

		@code
		# This phone number is too long.
		>>> DataMassager.checkPhone('88855512121')
		0

		@endcode

		@code
		# This phone number is too long.
		>>> DataMassager.checkPhone('188855512121')
		0

		@endcode
		"""

		data = DataMassager.stripPhone(data)

		if DataMassager.allNumbers(data) and \
		   (len(data) == 10 or (len(data) == 11 and data[0] == '1')):
			return True
		else:
			return False
	checkPhone = staticmethod(checkPhone)

	def cleanPhone(data):
		r"""
		Cleans the supplied @a data as a phone number.

		This method cleans the supplied @a data as a phone number. It
		strips out characters using the stripPhone() method. It also
		removes a leading @c 1 if one exists.

		@param data A string (or something that can be converted to a
		            string using the str() built-in) of data.

		@return     A cleaned phone number string.

		@exception  ValueError The specified @a data was not a valid
		                       phone number.

		@code
		>>> DataMassager.cleanPhone('8885551212')
		'8885551212'

		@endcode

		@code
		>>> DataMassager.cleanPhone('18885551212')
		'8885551212'

		@endcode

		@code
		>>> DataMassager.cleanPhone('888-555-1212')
		'8885551212'

		@endcode

		@code
		>>> DataMassager.cleanPhone('+1 (888) 555-1212')
		'8885551212'

		@endcode

		@code
		# This example shows that a phone number doesn't have to look
		# normal as long as only the allowed characters are used and it
		# has the right length after the extra characters are stripped
		# using the stripPhone() method.
		>>> DataMassager.cleanPhone('8((()8++--8-5(55-1+++21     2...')
		'8885551212'

		@endcode

		@code
		# This phone number contains illegal characters.
		>>> DataMassager.cleanPhone('#8885551212')
		Traceback (most recent call last):
		    ...
		ValueError: Not a valid phone number.

		@endcode

		@code
		# This phone number is too short.
		>>> DataMassager.cleanPhone('888555121')
		Traceback (most recent call last):
		    ...
		ValueError: Not a valid phone number.

		@endcode

		@code
		# This phone number is too long.
		>>> DataMassager.cleanPhone('88855512121')
		Traceback (most recent call last):
		    ...
		ValueError: Not a valid phone number.

		@endcode

		@code
		# This phone number is too long.
		>>> DataMassager.cleanPhone('188855512121')
		Traceback (most recent call last):
		    ...
		ValueError: Not a valid phone number.

		@endcode
		"""

		if not DataMassager.checkPhone(data):
			raise ValueError, 'Not a valid phone number.'

		data = DataMassager.stripPhone(data)

		if len(data) == 10:
			return data
		elif len(data) == 11 and data[0] == '1':
			return data[1:]
		else:
			# This error means that the logic right above doesn't
			# match the logic in the checkPhone method.
			assert 0, 'Phone number functions out of sync.'
	cleanPhone = staticmethod(cleanPhone)

	def formatPhone(data):
		r"""
		Formats a phone number.

		This method formats the supplied @a data as a phone number. It
		cleans the number using the cleanPhone() method.

		@param data A string (or something that can be converted to a
		            string using the str() built-in) of data.

		@return     A string of the form: @c (AAA) @c PPP-NNNN

		@exception  ValueError The specified @a data was not a valid
		                       phone number.

		@code
		>>> DataMassager.formatPhone('8885551212')
		'(888) 555-1212'

		@endcode

		@code
		>>> DataMassager.formatPhone('18885551212')
		'(888) 555-1212'

		@endcode

		@code
		>>> DataMassager.formatPhone('888-555-1212')
		'(888) 555-1212'

		@endcode

		@code
		>>> DataMassager.formatPhone('+1 (888) 555-1212')
		'(888) 555-1212'

		@endcode

		@code
		# This example shows that a phone number doesn't have to look
		# normal as long as only the allowed characters are used and it
		# has the right length after the extra characters are stripped
		# using the stripPhone() method.
		>>> DataMassager.formatPhone('8((()8++--8-5(55-1+++21     2...')
		'(888) 555-1212'

		@endcode

		@code
		# This phone number contains illegal characters.
		>>> DataMassager.formatPhone('#8885551212')
		Traceback (most recent call last):
		    ...
		ValueError: Not a valid phone number.

		@endcode

		@code
		# This phone number is too short.
		>>> DataMassager.formatPhone('888555121')
		Traceback (most recent call last):
		    ...
		ValueError: Not a valid phone number.

		@endcode

		@code
		# This phone number is too long.
		>>> DataMassager.formatPhone('88855512121')
		Traceback (most recent call last):
		    ...
		ValueError: Not a valid phone number.

		@endcode

		@code
		# This phone number is too long.
		>>> DataMassager.formatPhone('188855512121')
		Traceback (most recent call last):
		    ...
		ValueError: Not a valid phone number.

		@endcode
		"""

		data = DataMassager.cleanPhone(data)

		return '(' + data[0:3] + ') ' + data[3:6] + '-' + data[6:10]
	formatPhone = staticmethod(formatPhone)

	def stripPhone(data):
		r"""
		Strips extraneous user-entered characters from a phone number.

		This method strips characters from a phone number that would
		be expected from a user. In other words, this partially
		normalizes a phone number. It does not remove a leading @c 1
		like the cleanPhone() method does.

		@param data A string (or something that can be converted to a
		            string using the str() built-in) of data.

		@return     The supplied @a data with spaces and the following
		            characters removed: @c .()+-

		\note       The characters which are stripped are defined in
		            the __stripPhone regular expression near the top of
			    this file.

		@code
		>>> DataMassager.stripPhone('8885551212')
		'8885551212'

		@endcode

		@code
		>>> DataMassager.stripPhone('18885551212')
		'18885551212'

		@endcode

		@code
		>>> DataMassager.stripPhone('888-555-1212')
		'8885551212'

		@endcode

		@code
		>>> DataMassager.stripPhone('+1 (888) 555-1212')
		'18885551212'

		@endcode

		@code
		# This example shows that a phone number doesn't have to look
		# normal as long as only the allowed characters are used.
		>>> DataMassager.stripPhone('8((()8++--8-5(55-1+++21     2...')
		'8885551212'

		@endcode
		"""

		# NOTE: The definition of these characters is the __stripPhone
		#       regex above.

		if data == None:
			return None

		return DataMassager.__stripPhone.sub('', str(data))
	stripPhone = staticmethod(stripPhone)

def _test():
	r"""
	Test Method

	This method is used when this file is run stand-alone to perform unit
	tests with doctest. It also runs pychecker tests if pychecker is
	installed.
	"""
	__pychecker__ = 'no-reimportself no-reimport unusednames=pychecker'
	import doctest

	try:
		import pychecker.checker
	except ImportError:
		pass

	import DataMassager
	return doctest.testmod(DataMassager)

if __name__ == "__main__":
	_test()
