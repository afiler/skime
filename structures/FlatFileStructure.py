from Structure import *

class FlatFileStructure(Structure):
	r"""
	Flat File Structure Superclass

	Classes which inherit from this class represent records from flat files
	as a data structure. Instead of a database as the backend storage, data
	is kept in flat files with records of a fixed length.

	@remarks This class exists primarly to read legacy data. It would be
	         foolish for newly designed applications to store data in flat
	         files.
	"""

	def __init__(self,
	             filename,
		     formPrefix,
		     formTitle,
		     groupTitle,
	             defaultFieldArrangement='list',
	             headerLength=128,
	             fileFieldOrder=None):
		r"""
		Initialize a FlatFileStructure.

		This method stores the @a filename and @a headerLength for
		later use. It then calculates all the field offsets from the
		properties in @c allFields. Therefore, subclasses are expected

		@param filename                The filename of the flat file
		                               which holds the data.
		@param formPrefix              The prefix to use when building
		                               forms. This is typically
		                               @a formTitle without spaces.
		@param formTitle               The title to use when generating
		                               a form for just one of these
		                               structures.
		@param groupTitle              The title to use when generating
		                               a form for multiple instances of
		                               this structure. This is
		                               typically the plural of
		                               @a formTitle.
		@param defaultFieldArrangement The default field arrangement of
		                               this structure.
		@param headerLength            The length of the flat file
		                               header. (The header is skipped
		                               by this class when manipulating
		                               data.)
		@param fileFieldOrder          If the order of the fields in
		                               the flat file differs from the
		                               order of the fields in
		                               @c fieldOrder, @a fileFieldOrder
		                               must be specified as a list of
		                               fields in the order in which
		                               they appear in the file.

		@pre @a filename must not be @c None or the empty string.
		@pre @a formPrefix must not be @c None or the empty string.
		@pre @a formTitle must not be @c None or the empty string.
		@pre @a groupTitle must not be @c None or the empty string.
		@pre @a defaultFieldArrangementable must not be @c None or
		     the empty string.
		@pre @a headerLength must be an integer greater than or equal
		     to zero.
		"""
		assert (filename != None and filename != ''), \
		       'filename must not be None or the empty string.'

		assert (formPrefix != None and formPrefix != ''), \
		       'formPrefix must not be None or the empty string.'

		assert (formTitle != None and formTitle != ''), \
		       'formTitle must not be None or the empty string.'

		assert (groupTitle != None and groupTitle != ''), \
		       'groupTitle must not be None or the empty string.'

		assert (defaultFieldArrangement != None and \
		        defaultFieldArrangement != ''), \
		'defaultFieldArrangement must not be None or the empty string.'

		try:
			assert (int(headerLength) >= 0), \
			  'headerLength must be greater than or equal to zero.'
		except ValueError:
			assert 0, 'headerLength must be convertable to an int.'

		Structure.__init__(self,
		                   filename,
		                   formPrefix,
		                   formTitle,
		                   groupTitle,
		                   defaultFieldArrangement)

		self.fileHeader = int(headerLength)

		if fileFieldOrder != None:
			self.fileFieldOrder = fileFieldOrder
		else:
			self.fileFieldOrder = self.fieldOrder

		offset = 0
		for field in self.fileFieldOrder:
			if self.allFields[field].ffOffset == None:
				self.allFields[field].ffOffset = offset
			else:
				offset = self.allFields[field].ffOffset

			if self.allFields[field].maxlength != None:
				offset += self.allFields[field].maxlength
		self.recordLength = offset

		for field in self.fileFieldOrder:
			if self.allFields[field].ffGarbage:
				self.fileFieldOrder.remove(field)
				del self.allFields[field]


	def dbLoad(cls, env, con, query=None, where=None,
	           orderBy=None, reverseSort=False, max=None):
		r"""
		Generate records from @a con based on @a query dictionary.

		This method is used to retrieve data from the flat file.

		@param env         An instance of the @em env class which keeps
		                   track of the current operational
		                   environment.
		@param con         A dummy variable for rough compatibility
		                   with database structures. This variable is
		                   is ignored.
		@param query       A dictionary with fields as the keys and
		                   the values to match.
		@param where       A dummy variable for rough compatibility
		                   with database structures. This variable
		                   must be @c None.
		@param orderBy     A dummy variable for rough compatibility
		                   with database structures. This variable
		                   must be @c None.
		@param reverseSort A dummy variable for rough compatibility
		                   with database structures. This variable
		                   must be @c False.
		@param max         A dummy variable for rough compatibility
		                   with database structures. This variable
		                   must be @c None.

		@return Generates instances of the class on which this method
		        was called. Each instance will contain the data from
		        one row in the database.

		@pre @a query must contain at least one field that is valid in
		     the current configuration.
		@pre @a where must be @c None. (This feature is not supported
		     by the flat file engine.)
		@pre @a orderBy must be @c None. (This feature is not supported
		     by the flat file engine)
		@pre @a reverseSort must be @c False. (This feature is not
		     supported by the flat file engine.)
		@pre @a max must be @c None. (This feature is not supported by
		     the flat file engine.)
		"""
		assert where == None, \
		  'WHERE clauses are not supported by the flat file engine.'
		assert orderBy == None, \
		  'Sorting is not supported by the flat file engine.'
		assert not reverseSort, \
		  'Sorting is not supported by the flat file engine.'
		assert max == None, \
		  'A record cap is not supported by the flat file engine.'

		instance = cls(env)

		db = file(instance.dbTable)
		db.seek(instance.fileHeader)

		while True:
			row = db.read(instance.recordLength)
			if len(row) == 0: break

			if query != None and len(query) != 0:
				for field in query:
					if query[field] == instance.__getField(row, field):
						rec = cls(env)
						rec.dbLoadRecord(row)
						yield rec
			else:
				rec = cls(env)
				rec.dbLoadRecord(row)
				yield rec

		db.close()
	dbLoad = classmethod(dbLoad)

	def dbLoadRecord(self, row):
		r"""
		Load fields from a flat file record.

		This method takes a flat file record and loads the fields into
		the @c values variable.

		@param row The flat file row as a string.
		"""
		for field in self.fileFieldOrder:
			if self.allFields[field].maxlength != None:
				# This is not likely to ever have an effect
				# because the maxlength property does
				# double-duty for flat files: The length of
				# fields is fixed. The only time it could ever
				# get used is if the maxlength of a field was
				# set smaller than the actual length of the
				# field and the next field had a manually
				# entered ffOffset property that compensated.
				# I see no reason for this, but the current
				# code could let it happen and there's no
				# reason to be short-sighted.
				self.values[field] = \
				  (self.__getField(row, field))[ \
				  :self.allFields[field].maxlength]
			else:
				self.values[field] = \
				  self.__getField(row, field)

	def dbSave(self, env):
		r"""
		Save the record to the flat file.

		This method is not implemented.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.

		@exception NotImplementedError This method is not implemented.
		"""
		raise NotImplementedError, 'Flat File Saving Not Implemented'

	## protected:
	def dbGenerateSaveQuery(self, env):
		r"""
		Generates a query used to save a record to the database.

		This implementation returns @c None to indicate that the
		back-end data store is not an SQL database. Callers must use
		dbSave() directly.
		"""
	## public:

	def __getField(self, record, field):
		r"""
		Get a @a field from a flat file @a record.

		@param record The flat file record as a string.
		@param field  The name of the field to get.

		@return The @a field as a string, with whitespace stripped
		        from both ends.
		"""
		(offset, length) = (self.allFields[field].ffOffset, self.allFields[field].maxlength)
		return record[offset:offset+length].strip()
