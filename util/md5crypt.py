r"""
MD5 crypt() Functions

Recent versions of Unix-like operating systems have replaced the standard
crypt() password hashing with MD5 based hashing. These functions implement an
interoperatable function in pure Python code.

The following license applies:
 "THE BEER-WARE LICENSE" (Revision 42):
 <phk@login.dknet.dk> wrote this file.  As long as you retain this notice you
 can do whatever you want with this stuff. If we meet some day, and you think
 this stuff is worth it, you can buy me a beer in return.   Poul-Henning Kamp

@author Michal Wallace \<http://www.sabren.com\>
@author Carey Evans \<http://home.clear.net.nz/pages/c.evans/\>
@author Dennis Marti \<http://users.starpower.net/marti1/\>
@author Bryan Hart \<bryan\@eai.com\>
@version 0423.2000
"""

ITOA64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

import md5

def to64 (integer, count):
	r"""
	Encode @a integer into 6-bit string.

	This function encodes an integer into a string of characters. Each
	character is computed by using the least-significant 6 bits of the
	@a integer as an offset for the following list:
	@c "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

	@param integer The integer to convert.
	@param count   The number of 6-bit blocks to use. In essense, this is
	               the number of significant bits in the @a integer divided
	               by six (assuming that the number of significant bits has
	               been rounded up to a multiple of six and the @a integer
		       has been padded on the most-significant side with zeros
		       to match the appropriate number of significant bits
		       after rounding).
	"""
	__pychecker__ = 'unusednames=x'
	out = []
	for x in range(count):
		out.append(ITOA64[integer & 0x3f])
		integer = integer >> 6
	return ''.join(out)


def apache_md5_crypt (password, salt=None):
	r"""
	Apache MD5 Password Hasher

	This function calls unix_md5_crypt() with a @a magic of: @c '$apr1$'

	@param password The password to hash.
	@param salt     The salt to use to hash the password. If no @a salt is
	                provided, a random salt is generated. If @a salt starts
	                with @c '$apr1$', that magic will be stripped from
	                @a salt before processing. If @a salt is longer than 8
	                characters, it will be truncated.

	@pre @c password must not be None.

	@author Bryan Hart \<bryan@eai.com\>.

	@code
	>>> apache_md5_crypt('password', 'abc')
	'$apr1$abc$mehJE/UcwZsj.w5DYe.b5.'

	@endcode

	@code
	>>> apache_md5_crypt('password', '$apr1$abc')
	'$apr1$abc$mehJE/UcwZsj.w5DYe.b5.'

	@endcode
	"""
	return unix_md5_crypt(password, salt, '$apr1$')


def unix_md5_crypt(password, salt=None, magic=None):
	r"""
	MD5 Password Hasher

	This function provides a crypt()-compatible interface to the rather new
	MD5-based crypt() function found in modern operating systems. It's
	based on the implementation found on FreeBSD 2.2.5-RELEASE and the
	Crypt:<span></span>:PasswdMD5 module by Luis Munoz \<lem\@cantv.net\>.

	@param password The password to hash.
	@param salt     The salt to use to hash the password. If no @a salt is
	                provided, a random salt is generated. If @a salt starts
	                with @a magic, the @a magic is stripped from @a salt
	                before processing. If @a salt is longer than 8
	                characters, it will be truncated.
	@param magic    The magic string. If no magic string is provided, the
	                default string @c '$1$' is used.

	@pre @c password must not be None.

	@code
	>>> unix_md5_crypt('password', 'abc')
	'$1$abc$BXBqpb9BZcZhXLgbee.0s/'

	@endcode

	@code
	>>> unix_md5_crypt('password', 'abc', '$XYZ$')
	'$XYZ$abc$pLg9T5j2OATuq5rVaHMi1/'

	@endcode

	@code
	>>> unix_md5_crypt('password', '$1$abc')
	'$1$abc$BXBqpb9BZcZhXLgbee.0s/'

	@endcode

	"""
	__pychecker__ = 'no-noeffect unusednames=x'
	assert password != None, 'password cannot be None'

	if magic == None:
		magic = '$1$'
	else:
		magic = str(magic)

	if salt != None:
		salt = str(salt)
	else:
		salt = ''

	# Take care of the magic string if present
	if salt[:len(magic)] == magic:
		salt = salt[len(magic):]

	if salt == '':
		import random
		salt = ''.join([random.choice(ITOA64) for x in range(8)])
	else:
		# salt can have up to 8 characters:
		salt = salt.split('$', 1)[0]
		salt = salt[:8]

	ctx = password + magic + salt

	final = md5.md5(password + salt + password).digest()

	for pl in range(len(password),0,-16):
		if pl > 16:
			ctx = ctx + final[:16]
		else:
			ctx = ctx + final[:pl]

	# Now the 'weird' xform (??)

	i = len(password)
	while i:
		if i & 1:
			ctx = ctx + chr(0)
		else:
			ctx = ctx + password[0]
		i = i >> 1

	final = md5.md5(ctx).digest()

	# The following is supposed to make
	# things run slower.

	# my question: WTF???

	for i in range(1000):
		ctx1 = ''
		if i & 1:
			ctx1 = ctx1 + password
		else:
			ctx1 = ctx1 + final[:16]

		if i % 3:
			ctx1 = ctx1 + salt

		if i % 7:
			ctx1 = ctx1 + password

		if i & 1:
			ctx1 = ctx1 + final[:16]
		else:
			ctx1 = ctx1 + password

		final = md5.md5(ctx1).digest()


	# Final xform

	passwd = ''

	passwd = passwd + to64((int(ord(final[0])) << 16)
                              |(int(ord(final[6])) << 8)
                              |(int(ord(final[12]))),4)

	passwd = passwd + to64((int(ord(final[1])) << 16)
                              |(int(ord(final[7])) << 8)
                              |(int(ord(final[13]))), 4)

	passwd = passwd + to64((int(ord(final[2])) << 16)
                              |(int(ord(final[8])) << 8)
                              |(int(ord(final[14]))), 4)

	passwd = passwd + to64((int(ord(final[3])) << 16)
                              |(int(ord(final[9])) << 8)
                              |(int(ord(final[15]))), 4)

	passwd = passwd + to64((int(ord(final[4])) << 16)
                              |(int(ord(final[10])) << 8)
                              |(int(ord(final[5]))), 4)

	passwd = passwd + to64((int(ord(final[11]))), 2)


	return magic + salt + '$' + passwd

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

	import md5crypt
	return doctest.testmod(md5crypt)

if __name__ == "__main__":
	_test()
