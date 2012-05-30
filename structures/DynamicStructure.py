from Structure import *

class DynamicStructure(Structure):
	r"""
	Dynamic Data Structure Superclass

	This class implements the base functionality for data structures with
	dynamic properties. Subclasses of this class will implement
	functionality common to a set of related structures. Subclasses of
	those subclasses will have additional data fields. The key is that the
	varying columns will all be stored in the same back-end data structure.

	\class DynamicStructure
	@author Richard Laager \<rlaager\@wiktel.com\>
	"""

	## protected:
	def __init__(self,
		     dbTable,
		     formPrefix,
		     formTitle,
		     groupTitle,
	             defaultFieldArrangement='list',
		     dbLinkedServerName=None,
     		     dbPropertyTable=None):
		r"""
		DynamicStructure Constructor

		This constructor sets up a data structure. The various titles
		of the structure and the @c defaultFieldArrangement are saved.

		@param dbTable                 The title of the database table
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
		@param dbLinkedServerName      The name of the linked server
		                               which stores the data.
		@param dbPropertyTable         The title of the database table
		                               which holds the dynamic columns.
		                               Setting this argument to @c None
		                               is equivalent to setting it to
		                               the value of @a dbTable with
		                               @c Properties appended.

		@pre @a dbTable must not be @c None or the empty string.
		@pre @a formPrefix must not be @c None or the empty string.
		@pre @a formTitle must not be @c None or the empty string.
		@pre @a groupTitle must not be @c None or the empty string.
		@pre @a defaultFieldArrangementable must not be @c None or
		     the empty string.
		@pre The caller is expected to be a subclass which has already
		     setup the @c allFields and @c fieldOrder class variables.

		@remarks Linked servers are not currently supported for
		         DynamicStructure instances and likely never will be.
		"""

		assert dbLinkedServerName == None, \
		  'Linked servers are not supported for DynamicStructures.'

		self.dbDynamicTable = True

		if hasattr(self, 'allFields'):
			for key in self.allFields2:
				self.allFields[key] = self.allFields2[key]
			del key
		else:
			self.allFields = self.allFields2
			del self.allFields2

		if hasattr(self, 'fieldOrder'):
			self.fieldOrder2 = list(self.fieldOrder2)
			self.fieldOrder2.extend(self.fieldOrder)
			self.fieldOrder = tuple(self.fieldOrder2)
		else:
			self.fieldOrder = self.fieldOrder2
		del self.fieldOrder2

		Structure.__init__(self, dbTable, formPrefix, formTitle,
		                         groupTitle, defaultFieldArrangement)

		if dbPropertyTable:
			self.dbPropertyTable = dbPropertyTable
		else:
			self.dbPropertyTable = str(self.dbTable) + 'Properties'
		
		self.propertyNameColumn  = 'PropertyName'
		self.propertyValueColumn = 'PropertyValue'
	## public:

	def dbLoad(cls, env, con, query=None, where=None,
	           orderBy=None, reverseSort=False, max=None):
		r"""
		Generate records from @a con based on @a query dictionary
		and/or @a where condition.

		This method is used to retrieve data from the database.

		@param env         An instance of the @em env class which keeps
		                   track of the current operational
		                   environment.
		@param con         A DB-API connection to use to execute the
		                   SQL query.
		@param query       A dictionary with fields as the keys and
		                   the values to match. A WHERE clause will be
		                   constructed automatically. If the @a where
		                   argument is used at the same time as this
		                   argument, the @c WHERE clause will apply
				   first with the generated clause attached to
		                   the end of the @c WHERE clause with @c AND.
		@param where       A @c WHERE clause to apply to the query.
		@param orderBy     An iterable variable of fields to sort by.
		                   The sorting applies by the order of the
		                   fields iterated over.
		@param reverseSort If @c True, the sort will be reversed. In
		                   other words, it will be in descending order.
		                   This is accomplished by using @c DESC in the
		                   SQL query.
		@param max         The maximum number of records to match. This
		                   value will only be honored if using a DB-API
		                   driver supports the @c rowcount attribute.
		                   DB-API 1.0 drivers do not support the
		                   @c rowcount attribute.

		@return Generates instances of the class on which this method
		        was called. Each instance will contain the data from
		        one row in the database.

		@pre @a query must contain at least one field that is valid in
		     the current configuration.
		@pre @a max must be either @c None or an integer greater than
		     zero.

		@exception RuntimeError A @e RuntimeError will be thrown if
		                        the number of records matched is known
		                        and is greater than @a max.

		@todo Decide if @a con should be eliminated in favor of using
		      @c con from @a env. If so, implement this functionality.
		"""
		try:
			assert (max == None or int(max) > 0), \
			       'max must be greater than zero.'
		except ValueError:
			assert 0, 'max must be None or convertable to an int.'

		instance = cls(env)

		assert instance.findPK() != [], \
		  'A primary key is required for DynamicStructures.'

		properties = [x for x in instance.fields if instance.allFields[x].dbDynamicProperty == True]

		if where == None:
			where = []
		else:
			where = [where]

		args  = []
		if query != None:
			for key in query:
				if instance.allFields.has_key(key) and \
				   instance.allFields[key].present:
					if where != []:
						where.append(' AND ')
					where.append('"')
					if instance.allFields[key].dbDynamicProperty == False:
						where.append(instance.allFields[key].dbName)
					else:
						where.append('p')
						where.append(str(properties.index(key) + 1))
						where.append('"."')
						where.append(instance.propertyValueColumn)
					where.append('"=?')
					args.append(query[key])
			assert len(args) > 0, \
			       'No valid fields were present in query.' + \
			       str(query) + ' ' + str(instance.allFields.has_key(key)) + ' ' + \
			       str(instance.allFields)

		sql = []

		sql.append('SELECT ')
		if len(properties) > 0:
			sql.append('DISTINCT ')
		sql.append('"')
		sql.append(instance.dbTable)
		sql.append('"."')
		sql.append(('","' + instance.dbTable + '"."').join([instance.allFields[x].dbName for x in instance.fields if instance.allFields[x].dbDynamicProperty == False]))
		sql.append('"')

		index = 1
		for property in properties:
			sql.append(', CONVERT(')
			sql.append(instance.allFields[property].dbType)
			if instance.allFields[property].dbType == 'char' or \
			   instance.allFields[property].dbType == 'nchar' or \
			   instance.allFields[property].dbType == 'varchar' or \
			   instance.allFields[property].dbType == 'nvarchar':
				sql.append('(')
				sql.append(str(instance.allFields[property].maxlength))
				sql.append(')')
			sql.append(', "p')
			sql.append(str(index))
			sql.append('"."')
			sql.append(instance.propertyValueColumn)
			sql.append('") AS "')
			sql.append(instance.allFields[property].dbName)
			sql.append('"')
			index += 1

		sql.append(' FROM "')
		sql.append(instance.dbTable)
		sql.append('"')

		if len(properties) > 0:
			sql.append(',"')
			sql.append(instance.dbPropertyTable)
			sql.append('" "p0"')

			for i in xrange(1, index):
				sql.append(' FULL JOIN "')
				sql.append(instance.dbPropertyTable)
				sql.append('" "p')
				sql.append(str(i))
				sql.append('" ON (1=1')

				for field in instance.findPK():
					sql.append(' AND "p0"."')
					sql.append(instance.allFields[field].dbName)
					sql.append('" = "p')
					sql.append(str(i))
					sql.append('"."')
					sql.append(instance.allFields[field].dbName)
					sql.append('"')
				
				sql.append(') AND "p')
				sql.append(str(i))
				sql.append('"."')
				sql.append(instance.propertyNameColumn)
				sql.append('" = \'')
				sql.append(instance.allFields[properties[i-1]].dbName)
				sql.append('\'')

			sql.append(' WHERE 1=1')

			for field in instance.findPK():
				sql.append(' AND "')
				sql.append(instance.dbTable)
				sql.append('"."')
				sql.append(instance.allFields[field].dbName)
				sql.append('" = "p0"."')
				sql.append(instance.allFields[field].dbName)
				sql.append('"')

			for i in xrange(1, index):
				sql.append(' AND ("p')
				sql.append(str(i))
				sql.append('"."')
				sql.append(instance.propertyNameColumn)
				sql.append('" = \'')
				sql.append(instance.allFields[properties[i-1]].dbName)
				sql.append('\' OR "p')
				sql.append(str(i))
				sql.append('"."')
				sql.append(instance.propertyNameColumn)
				sql.append('" IS NULL)')

			if len(where) > 0:
				sql.append(' AND (')
				sql.extend(where)
				sql.append(')')
				where = None
		else:
			if len(where) > 0:
				sql.append(' WHERE ')
				sql.extend(where)
				where = None

		if orderBy != None and len(orderBy) > 0:
			sql.append(' ORDER BY ')
			orderByIndex = 1
			for x in orderBy:
				if orderByIndex > 1:
					sql.append(',')
				sql.append('"')
				if instance.allFields[x].dbDynamicProperty == False:
					sql.append(instance.dbTable)
					sql.append('"."')
				sql.append(instance.allFields[x].dbName)
				sql.append('"')
				orderByIndex += 1
			if reverseSort:
				sql.append(' DESC')

		cur = con.cursor()
		util.CursorWrapper.CursorWrapper.execute(cur, ''.join(sql), args)
		sql = None
		args = None

		# XXX: This is a work-around for DBAPI 1.0 compatibility.
		try:
			rowcount = cur.rowcount
			if (max != None and rowcount > max):
				raise RuntimeError, 'A maximum ' + str(max) + \
				      ' rows were requested but ' + \
				      str(rowcount) + ' were found.'
		except AttributeError:
			pass

		while 1:
			try:
				row = cur.fetchone()
			except:
				break
			if row != None:
				rec = cls(env)
				rec.dbLoadRecord(row)
				yield rec
			else:
				break

		cur.close()

	dbLoad = classmethod(dbLoad)

	## protected:
	def dbLoadRecord(self, row):
		r"""
		Load fields from a database row.

		This method takes a database @a row and loads the fields into
		the @c values variable.

		@param row The database row as a tuple of fields.
		"""
		for x, y in zip(self.fields, row):

			# Strip Strings
			if type(y) == type(''):
				y = y.strip()

				# Truncate Strings w/ a maxlength Property
				if self.allFields[x].maxlength:
					y = y[:self.allFields[x].maxlength]

			# Store the Value
			self.values[x] = y

	def dbGenerateSaveQuery(self, env):
		r"""
		Generates a query used to save a record to the database.

		If the record has values for one or more primary key fields, it
		is assumed that the record already exists in the database and
		an @c UPDATE query should be generated. Otherwise, an
		@c INSERT query is generated.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.

		@return This method returns a two element tuple consisting of
		        the SQL query needed to save the record to the
		        database and a list of arguments to the SQL query.
		        Subclasses which override this method may return
		        @c None to indicate that the back-end data store does
		        not use SQL. In such a case, the dbSave() method must
		        be called directly.

		@todo Extend this method so that inserts can be done when
		      a value exist for a primary key. This will allow
		      @c INSERTs to be done for tables with primary keys that
		      are not @c IDENTITY columns.
		"""
		mode = 'insert'

		where = []
		whereArgs = []

		PK = self.findPK()
		PK2 = list(PK)

		dbIdentityFound = False
		for key in PK2:
			if self.allFields[key].dbIdentity:
				assert not dbIdentityFound, \
				  'Only one IDENTITY column per table is allowed.'
				dbIdentityFound = True

			if (not self.values.has_key(key)) or \
		           (self.allFields[key].dbIdentity and \
		            self.values[key] == None \
		           ) or \
		           (self.values[key] != None and \
			    (self.allFields[key].dbType == 'datetime' or \
		             self.allFields[key].dbType == 'image' or \
		             self.allFields[key].dbType == 'ntext' or \
		             self.allFields[key].dbType == 'text' \
		            ) \
		           ):
				PK.remove(key)
			

		if len(PK) > 0:
			mode = 'update'

			for key in PK:
				if where != []:
					where.append(' AND ')
				where.append('"')
				where.append(self.allFields[key].dbName)
				where.append('"')

				if self.values[key] == None:
					where.append(' IS NULL')
				else:
					where.append('=?')
					whereArgs.append(self.values[key])

		sql = []

		sql.append('BEGIN TRANSACTION; ')

		if mode == 'update':
			sql.append('DELETE FROM "')
			sql.append(self.dbPropertyTable)
			sql.append('" WHERE ')
			sql.extend(where)
			sql.append('; UPDATE "')
			sql.append(self.dbTable)
			sql.append('" SET "')
			sql.append('"=?,"'.join([self.allFields[x].dbName \
			      for x in self.fields \
			      if (not self.allFields[x].dbIdentity) \
			         and self.values.has_key(x) \
				 and (not self.allFields[x].dbDynamicProperty)]))
			sql.append('"=? WHERE ')
			sql.extend(where)
			sql.append('; ')
		elif mode == 'insert':
			sql.append('INSERT INTO "')
			sql.append(self.dbTable)
			sql.append('" ("')
			sql.append('","'.join([self.allFields[x].dbName \
			      for x in self.fields \
			      if (not self.allFields[x].dbIdentity) \
			         and self.values.has_key(x) \
				 and (not self.allFields[x].dbDynamicProperty)]))
			sql.append('") VALUES (')
			sql.append(','.join(['?' \
			      for x in self.fields \
			      if (not (self.allFields[x].dbIdentity \
			               or self.allFields[x].dbDynamicProperty)) \
			         and self.values.has_key(x)]))
			sql.append(');')

		for field in self.fields:
			if not self.allFields[field].dbDynamicProperty:
				continue
			sql.append('INSERT INTO "')
			sql.append(self.dbPropertyTable)
			sql.append('" ("')
			sql.append('","'.join([self.allFields[x].dbName for x in PK2]))
			sql.append('","')
			sql.append(self.propertyNameColumn)
			sql.append('","')
			sql.append(self.propertyValueColumn)
			sql.append('") VALUES (')
			for x in PK2:
				if self.allFields[x].dbIdentity and \
				   not self.values.has_key(x):
					sql.append('@@identity,')
				else:
					sql.append('?,')
			sql.append('?,?);')

		sql.append('COMMIT; ')

		args = []

		args.extend(whereArgs)

		for x in self.fields:
			if (not self.values.has_key(x)) or \
			   self.allFields[x].dbIdentity or \
			   self.allFields[x].dbDynamicProperty:
				continue
			if self.allFields[x].maxlength and \
			   type(self.values[x]) == type(''):
				args.append((self.values[x])[ \
				  :self.allFields[x].maxlength])
			else:
				args.append(self.values[x])

		args.extend(whereArgs)

		pkArgs = []
		for x in PK2:
			if self.allFields[x].dbIdentity and \
			   not self.values.has_key(x):
				continue
			if self.allFields[x].maxlength and \
			   type(self.values[x]) == type(''):
				pkArgs.append((self.values[x])[ \
				  :self.allFields[x].maxlength])
			else:
				pkArgs.append(self.values[x])

		for x in self.fields:
			if not self.allFields[x].dbDynamicProperty:
				continue
			args.extend(pkArgs)

			args.append(self.allFields[x].dbName)
			if self.allFields[x].maxlength and \
			   type(self.values[x]) == type(''):
				args.append((self.values[x])[ \
				  :self.allFields[x].maxlength])
			else:
				args.append(self.values[x])

		return (''.join(sql), args)
	## public: