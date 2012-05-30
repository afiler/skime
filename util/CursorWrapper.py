class CursorWrapper(object):
	r"""
	Provides methods that convert from one DB-API param style to another
	in the course of executing an SQL query.

	This class exists because the Python DB-API values simplicity in the
	drivers. Drivers are not expected to convert a parameter style from
	the application to the underlying database's native parameter style.
	This is great for driver writers, but bad for portability between
	databases. This class allows parameters to be converted on the fly.

	@author Richard Laager \<rlaager\@wiktel.com\>
	"""

	try:
		# XXX: This is for the dbiDate work-around below.
		import dbi
		__dbiDateType = type(dbi.dbiDate(0))
	except:
		__dbiDateType = None

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

	def convert(sql,
		    params=None,
		    fromParamStyle='qmark',
		    toParamStyle=None,
		    singleQuoteEscape="''"
		   ):
		r"""
		Convert the paramaters of an SQL query from one style to
		another.

		Valid parameter styles are:
		  - format   %s
		  - named    :value
		  - numeric  :1
		  - pyformat %(value)s
		  - qmark    ?

		These parameter styles must be provided as a string exactly as
		specified above. If an invalid parameter style is provided,
		an exception may be raised, but this behavior must not be
		relied upon.

		The parameter type @c None is also supported for the
		@a toParamStyle. Specifying the @c None parameter style tells
		the method to rewrite the query so that the parameter values
		are included in the SQL query.

		If @a fromParamStyle is the same as @a toParamStyle, the query
		is returned with no conversion.

		@param sql                The SQL query to convert.
		@param params             The parameters for the SQL query.
		@param fromParamStyle     The parameter style used in the
		                          query.
		@param toParamStyle       The parameter style used by the
		                          underlying database.
		@param singleQuoteEscape  The string used to replace single
		                          quotes in the params when the
					  @a toParamStyle is 'none'. Examples
					  would be: '' (double-single quotes),
					  \' (backslash-escaped single quote)

		@pre @a fromParamStyle and @a toParamStyle must be valid
		     parameter styles as defined above.

		@remarks This method currently only supports conversions from
		         the @c 'qmark' parameter style to the @c None
		         pseudo-style.

		@todo Implement the other possible conversions.
		"""

		if (fromParamStyle == toParamStyle):
			return sql

		assert fromParamStyle == 'format' or \
		       fromParamStyle == 'named' or \
		       fromParamStyle == 'numeric' or \
		       fromParamStyle == 'pyformat' or \
		       fromParamStyle == 'qmark', \
		       'fromParamStyle is an invalid parameter style.'

		assert toParamStyle == 'format' or \
		       toParamStyle == 'named' or \
		       toParamStyle == 'numeric' or \
		       toParamStyle == 'pyformat' or \
		       toParamStyle == 'qmark' or \
		       toParamStyle == None, \
		       'toParamStyle is an invalid parameter style.'

		# Temporary: Pending implementation of other conversions.
		assert fromParamStyle == 'qmark' and toParamStyle == None, \
			'Unsupported conversion.'

		if sql.count('?') == 0:
			return sql
		else:
			sql2 = []
			placeholder = 0
			placeholder2 = 0
			count = 0
			while 1:
				placeholder2 = sql.find('?', placeholder)
				if placeholder2 == -1:
					sql2.append(sql[placeholder:])
					break
				sql2.append(sql[placeholder:placeholder2])
				sql2.append("'")

				# XXX: This is a work-around for the ODBC
				# driver not taking its own dbiDate objects
				# back.
				if CursorWrapper.__dbiDateType != None and \
				   params[count] != None and \
				   type(params[count]) == \
				   CursorWrapper.__dbiDateType:
					sql2.append((str( \
						params[count])[4:]).replace( \
						"'", singleQuoteEscape))
				else:
					sql2.append(str( \
						params[count]).replace( \
						"'", singleQuoteEscape))

				sql2.append("'")
				placeholder = placeholder2 + 1
				count += 1
			return ''.join(sql2)
	convert = staticmethod(convert)

	def execute(cur,
	            sql,
		    params=None,
		    fromParamStyle='qmark',
		    toParamStyle=None,
		    singleQuoteEscape="''"
		   ):
		r"""
		Execute an SQL query after converting the parameters from one
		parameter style to another.

		Valid parameter styles are:
		  - format   %s
		  - named    :value
		  - numeric  :1
		  - pyformat %(value)s
		  - qmark    ?

		These parameter styles must be provided as a string exactly as
		specified above. If an invalid parameter style is provided,
		an exception may be raised, but this behavior must not be
		relied upon.

		The parameter type @c None is also supported for the
		@a toParamStyle. Specifying the @c None parameter style tells
		the method to rewrite the query so that the parameter values
		are included in the SQL query.

		If @a fromParamStyle is the same as @a toParamStyle, the query
		is executed with no conversion.

		@param cur                The DB-API cursor to use to execute
		                          the query.
		@param sql                The SQL query to execute.
		@param params             The parameters for the SQL query.
		@param fromParamStyle     The parameter style used in the
		                          query.
		@param toParamStyle       The parameter style used by the
		                          underlying database.
		@param singleQuoteEscape  The string used to replace single
		                          quotes in the params when the
					  @a toParamStyle is 'none'. Examples
					  would be: '' (double-single quotes),
					  \' (backslash-escaped single quote)

		@pre @a fromParamStyle and @a toParamStyle must be valid
		     parameter styles as defined above.

		@remarks This method currently only supports conversions from
		         the @c 'qmark' parameter style to the @c None
		         pseudo-style.

		@todo Handle the other possible conversions.
		"""

		if (fromParamStyle == toParamStyle):
			cur.execute(sql)
			return

		assert fromParamStyle == 'format' or \
		       fromParamStyle == 'named' or \
		       fromParamStyle == 'numeric' or \
		       fromParamStyle == 'pyformat' or \
		       fromParamStyle == 'qmark', \
		       'fromParamStyle is an invalid parameter style.'

		assert toParamStyle == 'format' or \
		       toParamStyle == 'named' or \
		       toParamStyle == 'numeric' or \
		       toParamStyle == 'pyformat' or \
		       toParamStyle == 'qmark' or \
		       toParamStyle == None, \
		       'toParamStyle is an invalid parameter style.'

		# Temporary: Pending implementation of other conversions.
		assert fromParamStyle == 'qmark' and toParamStyle == None, \
			'Unsupported conversion.'

#		if sql[0:22] != 'SELECT "InternalUserID':
#			assert 0, sql

		if sql.count('?') == 0:
			cur.execute(sql)
		else:
			cur.execute(CursorWrapper.convert(sql, params,
			                    fromParamStyle, toParamStyle,
					    singleQuoteEscape))
	execute = staticmethod(execute)

	def executemany(cur,
	                sql,
	                params_seq=None,
	                fromParamStyle='qmark',
	                toParamStyle='none',
			singleQuoteEscape="''"
		       ):
		r"""
		Execute an SQL query for multiple parameter sets after
		converting the parameters from one parameter style to another.

		Valid parameter styles are:
		  - format   %s
		  - named    :value
		  - numeric  :1
		  - pyformat %(value)s
		  - qmark    ?

		These parameter styles must be provided as a string exactly as
		specified above. If an invalid parameter style is provided,
		an exception may be raised, but this behavior must not be
		relied upon.

		The parameter type 'none' is also supported for the
		@a toParamStyle. Specifying the 'none' parameter style tells
		the method to rewrite the query so that the parameter values
		are included in the SQL query.

		If @a fromParamStyle is the same as @a toParamStyle, the query
		is executed with no conversion.

		@param cur                The DB-API cursor to use to execute
		                          the query.
		@param sql                The SQL query to execute.
		@param params_seq         The sequence of parameters for the
		                          SQL query.
		@param fromParamStyle     The parameter style used in the
		                          query.
		@param toParamStyle       The parameter style used by the
		                          underlying database.
		@param singleQuoteEscape  The string used to replace single
		                          quotes in the params when the
					  @a toParamStyle is 'none'. Examples
					  would be: '' (double-single quotes),
					  \' (backslash-escaped single quote)

		@pre @a fromParamStyle and @a toParamStyle must be valid
		     parameter styles as defined above.

		@remarks This method currently only supports conversions from
		         the @c 'qmark' parameter style to the @c None
		         pseudo-style.

		@todo Implement the other possible conversions.
		"""

		if (fromParamStyle == toParamStyle):
			cur.executemany(sql, params_seq)
			return

		assert fromParamStyle=='qmark' and toParamStyle=='none', \
			'Unsupported conversion.'

		if sql.count('?') == 0:
			cur.executemany(sql, params_seq)
		else:
			for params in params_seq:
				CursorWrapper.execute(cur, sql, params,
					fromParamStyle, toParamStyle,
					singleQuoteEscape)
	executemany = staticmethod(executemany)

def __isprivate(prefix, base):
	r"""
	Doctest Workaround

	This method returns @c False if @a base is @c 'dbi'. Otherwise, it
	returns whatever doctest.is_private() returns.

	This is a workaround for a doctest issue with dbi which stems from the
	dbi work-around involving dates. (See the code at the top of this file.)
	"""
	if base == 'dbi':
		return False
	import doctest
	return doctest.is_private(prefix, base)

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

	import CursorWrapper
	return doctest.testmod(CursorWrapper, isprivate=__isprivate)

if __name__ == "__main__":
	_test()
