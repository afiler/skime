import math

from display.html import *
from structures.fp import fp
from structures.disp import disp

import util.CursorWrapper

class Structure:
	r"""
	Data Structure Superclass

	This class is the base class for all data structures. A data structure
	is an object representation of a set of related data. Typically, this
	data would be stored in a database table, but other storage forms may
	be used. Methods exist to allow data to be retrieved and stored.

	\class Structure
	@author Andy Filer \<andyf\@wiktel.com\>
	@author Richard Laager \<rlaager\@wiktel.com\>
	"""

	## protected:
	def __init__(self,
		     dbTable,
		     formPrefix,
		     formTitle,
		     groupTitle,
	             defaultFieldArrangement='list',
	             dbLinkedServerName=None):
		r"""
		Structure Constructor

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

		@pre @a dbTable must not be @c None or the empty string.
		@pre @a formPrefix must not be @c None or the empty string.
		@pre @a formTitle must not be @c None or the empty string.
		@pre @a groupTitle must not be @c None or the empty string.
		@pre @a defaultFieldArrangementable must not be @c None or
		     the empty string.
		@pre The caller is expected to be a subclass which has already
		     setup the @c allFields and @c fieldOrder class variables.
		"""
		assert (dbTable != None and dbTable != ''), \
		       'dbTable must not be None or the empty string.'

		assert (formPrefix != None and formPrefix != ''), \
		       'formPrefix must not be None or the empty string.'

		assert (formTitle != None and formTitle != ''), \
		       'formTitle must not be None or the empty string.'

		assert (groupTitle != None and groupTitle != ''), \
		       'groupTitle must not be None or the empty string.'

		assert (defaultFieldArrangement != None and \
		        defaultFieldArrangement != ''), \
		'defaultFieldArrangement must not be None or the empty string.'

		assert hasattr(self, 'allFields'), \
		  'allFields class variable does not exist.'
		assert hasattr(self, 'fieldOrder'), \
		  'fieldOrder class variable does not exist.'

		self.dbTable    = dbTable
		self.formPrefix = formPrefix
		self.formTitle  = formTitle
		self.groupTitle = groupTitle

		self.defaultFieldArrangement = defaultFieldArrangement
		self.dbLinkedServerName = dbLinkedServerName

		self.dbConstraints   = ''
		self.dbMiscellaneous = ''
	## public:

	# START Utilty Methods Section

	## protected:
	def buildFields(self):
		r"""
		Build Fields

		This method initializes the @c fields and @c values variables
		by looping through @c fieldOrder and setting up all @c present
		fields.

		@post At least one field must be present.
		"""
		self.fields = [x for x in self.fieldOrder \
		               if self.allFields[x].present]
		self.values = {}
		assert len(self.fields) > 0, 'Zero fields were present.'
	## public:

	# END Utility Methods Section

	# START Database Classes Section

	def dbTriggers(self, env):
		r"""
		Generate database triggers.

		This method is a stub. Subclasses may override it to generate
		database trigger code.

		@param env An instance of the @em env class which keeps track
		                   of the current operational environment.
		"""
		return ''

	def dbDelete(self, cur):
		r"""
		Delete the record from the database.

		This method deletes a record from the database. The record is
		identified by its primary key(s) as determined by findPK(). If
		no primary key exists, all of the fields that can be compared
		will be compared. As a result, if no primary key exists,
		multiple records may be deleted.

		Fields with the following database types cannot be compared:
		 - datetime
		 - image
		 - ntext
		 - text

		@remarks In the case where no primary key exists, the behavior
		         of deleting all matching records should not be
		         considered a bug. If the database has been designed
		         without allowing records to be uniquely identified, it
			 should be no surprise that they can't be.

		@todo This needs support for linked servers.
		@todo This needs to be broken up into dbDelete() and
		      dbGenerateDeleteQuery().
		"""

		sql = 'DELETE FROM "' + self.dbTable + '" WHERE '
		where = ''
		args = []

		PK = self.findPK()
		for key in PK:
			if (not self.values.has_key(key)) or \
		           (self.allFields.dbIdentity and \
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
			fields = PK
		else:
			fields = self.fields

		for key in fields:
			if not self.values.has_key(key):
				continue

			if where != '':
				where += ' AND '
			where += '"' + self.allFields[key].dbName + '"'
			if self.values[key] == None:
				where += ' IS NULL'
			else:
				where += '=?'
				args.append(self.values[key])

		sql += where

		util.CursorWrapper.CursorWrapper.execute(cur, sql, args)
		# XXX: This is a work-around for DBAPI 1.0 compatibility.
		if hasattr(cur, 'commit'):
			cur.commit()

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
					where.append('[')
					where.append(instance.allFields[key].dbName)
					where.append(']')
					where.append('=?')
					args.append(query[key])
			assert len(args) > 0, \
			       'No valid fields were present in query.' + \
			       str(query) + ' ' + str(instance.allFields.has_key(key)) + ' ' + \
			       str(instance.allFields)

		sql = []
		sql.append('SELECT [')
		sql.append('],['.join( \
		       [instance.allFields[x].dbName \
			for x in instance.fields]))
		sql.append(']')

		sql.append(' FROM [')
		sql.append(instance.dbTable)
		sql.append(']')

		if len(where) > 0:
			sql.append(' WHERE ')
			sql.extend(where)
			where = None

		if orderBy != None and len(orderBy) > 0:
			sql.append(' ORDER BY [')
			sql.append('],['.join( \
			       [instance.allFields[x].dbName \
				for x in orderBy]))
			sql.append(']')
			if reverseSort:
				sql.append(' DESC')

		cur = env.con.cursor()
		if instance.dbLinkedServerName != None:
			sql = util.CursorWrapper.CursorWrapper.convert(''.join(sql), args)
			del args
			sql2 = []
			sql2.append('SELECT * FROM OPENQUERY("')
			sql2.append(str(instance.dbLinkedServerName))
			sql2.append('", \'')
			sql2.append(sql.replace("'", "''"))
			sql2.append('\')')
			sql = ''.join(sql2)
			del sql2
			cur.execute(sql)
			del sql
		else:
			util.CursorWrapper.CursorWrapper.execute(cur, ''.join(sql), args)
			del sql
			del args

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
	## public:

	def dbSave(self, env):
		r"""
		Save the record to the database.

		If the record has values for one or more primary key fields, it
		is assumed that the record already exists in the database and
		an @c UPDATE should be performed. Otherwise, an @c INSERT is
		performed.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""

		queryComponents = self.dbGenerateSaveQuery(env)
		assert queryComponents != None, \
		  'If dbGenerateSaveQuery() is overridden to return None, dbSave() must be overridden as well.'
		(sql, args) = queryComponents

		# TEMP: Debugging Code
		debug = 'SQL String is: ' + sql + ', ' + str(args)
		if env.req:
			env.req.write(debug)
		else:
			print debug

		#cur = env.con.cursor()
		#util.CursorWrapper.CursorWrapper.execute(cur, sql, args)
		# XXX: This is a work-around for DBAPI 1.0 compatibility.
		#if hasattr(cur, 'commit'):
		#	cur.commit()

	## protected:
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

		@todo This needs support for linked servers.
		@todo Extend this method so that inserts can be done when
		      a value exist for a primary key. This will allow
		      @c INSERTs to be done for tables with primary keys that
		      are not @c IDENTITY columns.
		"""
		mode = 'insert'

		args = []
		for x in self.fields:
			if (not self.values.has_key(x)) or \
			   self.allFields[x].dbIdentity:
				continue
			if self.allFields[x].maxlength and \
			   type(self.values[x]) == type(''):
				args.append((self.values[x])[ \
				  :self.allFields[x].maxlength])
			else:
				args.append(self.values[x])

		where = []

		PK = self.findPK()

		# We use list(PK) here because deleting keys from a list while
		# looping over it causes incorrect results.
		for key in list(PK):
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
					args.append(self.values[key])

		sql = []
		if mode == 'update':
			sql.append('UPDATE "')
			sql.append(self.dbTable)
			sql.append('" SET "')
			sql.append('"=?,"'.join([self.allFields[x].dbName \
			      for x in self.fields \
			      if (not self.allFields[x].dbIdentity) \
			         and self.values.has_key(x)]))
			sql.append('"=? WHERE ')
			sql.extend(where)
		elif mode == 'insert':
			sql.append('INSERT INTO "')
			sql.append(self.dbTable)
			sql.append('" ("')
			sql.append('","'.join([self.allFields[x].dbName \
			      for x in self.fields \
			      if (not self.allFields[x].dbIdentity) \
			         and self.values.has_key(x)]))
			sql.append('") VALUES (')
			sql.append(','.join(['?' \
			      for x in self.fields \
			      if (not self.allFields[x].dbIdentity) \
			         and self.values.has_key(x)]))
			sql.append(')')

		return (''.join(sql), args)
	## public:

	def findPK(self):
		r"""
		Find the primary key(s).

		@return A list of the field names where @c dbPrimaryKey is set
		        in @c allFields.
		"""
		return [x for x in self.fields \
		        if self.allFields[x].dbPrimaryKey]

	# END Database Methods Section

	# START Form Loading Methods Section

	def buildQuery(cls, env, max=1):
		r"""
		Builds a query dictionary based on data from an HTML form.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		@param max The maximum number of of form elements to process.

		@return Returns a dictionary of key value pairs based on the
		        data submitted from the form.

		@exception RuntimeError If the count of form elements is
		                        greater than @a max, an exception will
		                        be raised.

		@pre @a max must be either @c None or an integer greater than
		     zero.

		@remarks I don't know that this is even useful in something
		         other than a search object.
		"""
		try:
			assert (max == None or int(max) > 0), \
			       'max must be greater than zero.'
		except ValueError:
			assert 0, 'max must be None or convertable to an int.'

		instance = cls(env)
		if env.fieldStorage.has_key(instance.formPrefix+'.count'):
			count = int(env.fieldStorage[ \
			        instance.formPrefix+'.count'])
		else:
			raise RuntimeError, 'There is no form value for ' + \
			                    instance.formPrefix + '.count.'

		if max != None and count > max:
			raise RuntimeError, \
			      'Too many form entries were found.'

		query = {}
		for i in range(count):
			for field in instance.fields:
				formFieldName = instance.formPrefix + \
				                 '.' + field + '.' + str(i)
				if env.fieldStorage.has_key(formFieldName) \
				   and len( \
				     env.fieldStorage[formFieldName].strip() \
				   ) > 0:
					query[(instance.dbTable, field)] = \
					  env.fieldStorage[formFieldName]

		return query
	buildQuery = classmethod(buildQuery)

	def formLoad(cls, env, max=None):
		r"""
		Generate records from an HTTP GET/POST request.

		This method is used to retrieve data from a form submission.

		@param env An instance of the @em env class which keeps track of the current operational environment.
		@param max The maximum number of records to match.

		@pre @a max must be either @c None or an integer greater than zero.

		@exception RuntimeError A @e RuntimeError will be thrown if the number of records is greater than @a max.
		"""

		try:
			assert (max == None or int(max) > 0), \
			       'max must be greater than zero.'
		except ValueError:
			assert 0, 'max must be None or convertable to an int.'


		instance = cls(env)
		if env.fieldStorage.has_key(instance.formPrefix+'.count'):
			count = int(env.fieldStorage[instance.formPrefix + \
			                             '.count'])
		else:
			count = 0

		if (max != None and count > max):
			raise RuntimeError, 'A maximum ' + str(max) + \
			      ' rows were requested but ' + \
			      str(count) + ' were found.'

		for i in range(count):
			rec = cls(env)
			rec.formLoadRecord(env.fieldStorage, i, \
			                   instance.formPrefix)
			yield rec
	formLoad = classmethod(formLoad)

	## protected:
	def formLoadRecord(self, fs, index, title, strict=False):
		r"""
		Load fields from an HTTP GET/POST request.

		This method takes a database @a row and loads the fields into
		the @c values variable.

		@param fs     A @em FieldStorage instance with the data from
		              the HTTP request.
		@param index  The index of this form in relation to other forms
		              for the same data structure.
		@param title  The title of the elements in the form.
		@param strict A boolean indicating if the form should be loaded
		              according to strict standards. If true, all the
		              fields must exist or a @e RuntimeError will be
		              raised. In addition, all of the fields must be
		              less than or equal to the maximum length allowed
		              for the field. Basically, this function enforces
		              the assumption that we are getting a set of data
		              from the client that is consistent with the form
		              they should have been sent. If @a strict is
		              false, missing fields will not be considered an
		              error and over-length fields will be truncated.

		@exception RuntimeError @a strict was true and a field was not
		                        found in the GET/POST request data.
		@exception RuntimeError @a strict was true and a field was
		                        longer than its specified @c maxlength
		                        property.

		@remarks Callers should not expect that setting @a strict to
		         @c True will protect against attacks nor should
		         callers be afraid that setting @a strict to @c False
		         will open security holes.
		"""

		for field in self.fields:
			formFieldName = title+'.'+field+'.'+str(index)

			if fs.has_key(formFieldName):
				if self.allFields[field].maxlength:
					if strict and \
					   len(fs[formFieldName]) > \
					   self.allFields[field].maxlength:
						raise RuntimeError, \
					          'Form field was too long: ' \
					          + formFieldName

					self.values[field] = \
					  (fs[formFieldName])[ \
					  :self.allFields[field].maxlength]
				else:
					self.values[field] = fs[formFieldName]
			elif strict:
				raise RuntimeError, \
				  'No form value was found for ' + \
				  formFieldName
	## public:

	# END Form Loading Methods Section

	# START getForm Helpers Section

	def getPrintingFields(self, arrangement):
		r"""
		Get all the fields that will print in a given @a arrangement.

		@param arrangement The arrangement in question.

		@return A list of all the fields which will print in the
		        specified @a arrangement.
		"""

		return [f for f in self.fields \
		        if self.isPrintingField(f, arrangement)]

	def getDispTitle(self, fieldName, arrangement=None, editable=False):
		r"""
		Custom Display Title Handler

		This method handles titles for fields with a custom display type.

		@param fieldName The name of the field for which to generate
		                 display code.
		@param arrangement The arrangement to get the title row for. If
		                   no @a arrangement is provided, the
		                   @c defaultFieldArrangement will be used.
		@param editable    Will the form that this title row is for be editable?
		"""

		field = self.allFields[fieldName]
		display = field.display

		if  display.type == 'dbDropdown' or \
		   (display.type == 'dbLookup' and not (editable and field.editable)):
			instance = display.table(None)
			return instance.allFields[display.displayField].title

		return field.title

	def getDispElement(self, env, fieldName, formFieldName, editable=False):
		r"""
		Custom Display Element Handler

		This method handles fields with a custom display type.
		Currently, the types handled are @c dbDropdown (dropdown
		menus populated with data from the database), @c dbLookup
		(in non-editable mode, a lookup is performed in some table for
		the field's value; in editable mode, the value is displayed),
		and @c staticDropDown (dropdown menus populated by static data
		provided in the field's properties).

		@param env       An instance of the @em env class which keeps
		                 track of the current operational environment.
		@param fieldName The name of the field for which to generate
		                 display code.
		@param formFieldName	The name of the field to be used in
					the HTML form.  This is usually the
					form name prepended to, and the field
					sequence number appended to the field
					name.
		@param editable  A boolean indicating if the form should
		                 include elements for editing the fields or if
		                 it should just show the fields.

		@return HTML code implementing the custom display or @c None if
		        the caller should fall back to the non-custom default
		        display.
		"""

		field = self.allFields[fieldName]
		display = field.display

		if display.type == 'dbDropdown':

			instance = display.table(env)

			sql = 'SELECT [' + instance.allFields[ \
			                   display.displayField].dbName + \
			      '],[' + instance.allFields[ \
			              display.dataField].dbName + \
			       '] FROM ' + instance.dbTable

			if not editable and self.values.has_key(fieldName):
				if display.query != None:
					display.query[display.dataField] = \
					  self.values[fieldName]
				else:
					display.query = { \
					  display.dataField: \
					    self.values[fieldName]}

			where = display.where
			if where == None:
				where = ''

			args  = []
			if display.query != None:
				for key in display.query:
					if instance.allFields.has_key(key) \
					   and instance.allFields[key].present:
						if where != '':
							where += ' AND '
						where += '[' + \
						  instance.allFields[ \
						    key].dbName + ']=?'
						args.append(display.query[key])
				assert len(args) > 0, \
				  'No fields were present in display.query.'

			if where != '':
				sql += ' WHERE ' + where

			sql += ' ORDER BY [' + instance.allFields[ \
			                       display.displayField].dbName + \
			       '],[' + instance.allFields[ \
			               display.dataField].dbName + ']'

			cur = env.con.cursor()
			util.CursorWrapper.CursorWrapper.execute(cur, sql, args)
			result = cur.fetchall()
			cur.close()

			if not editable:
				if self.values.has_key(fieldName):
					return [x[0] for x in result \
					        if x[1] == self.values[ \
					        fieldName]][0]
				else:
					return ''
			else:
				if self.values.has_key(fieldName):
					return dropDown(name=formFieldName, \
					               values=[x[1] \
					               for x in result], \
					               titles=[x[0] \
					               for x in result], \
						       default=self.values[ \
					               fieldName])
				else:
					return dropDown(name=formFieldName, \
					               values=[x[1] \
					               for x in result], \
					               titles=[x[0] \
					               for x in result])
		elif display.type == 'dbLookup':

			instance = display.table(env)

			sql = 'SELECT TOP 1 [' + instance.allFields[ \
			                   display.displayField].dbName + \
			      '],[' + instance.allFields[ \
			              display.dataField].dbName + \
			       '] FROM ' + instance.dbTable

			if (not self.values.has_key(fieldName)) or (editable and self.allFields[fieldName].editable):
				return None

			if display.query != None:
				display.query[display.dataField] = \
				  self.values[fieldName]
			else:
				display.query = { \
				  display.dataField: \
				    self.values[fieldName]}

			where = display.where
			if where == None:
				where = ''

			args  = []
			if display.query != None:
				for key in display.query:
					if instance.allFields.has_key(key) \
					   and instance.allFields[key].present:
						if where != '':
							where += ' AND '
						where += '[' + \
						  instance.allFields[ \
						    key].dbName + ']=?'
						args.append(display.query[key])
				assert len(args) > 0, \
				  'No fields were present in display.query.'

			if where != '':
				sql += ' WHERE ' + where

			sql += ' ORDER BY [' + instance.allFields[ \
			                       display.displayField].dbName + \
			       '],[' + instance.allFields[ \
			               display.dataField].dbName + ']'

			cur = env.con.cursor()
			util.CursorWrapper.CursorWrapper.execute(cur, sql, args)
			result = cur.fetchall()
			cur.close()

			return result[0][0]

		elif display.type == 'staticDropdown':
			if not editable:
				if self.values.has_key(fieldName):
					try:
						return display.staticOptions[ \
							 self.values[ \
						         fieldName]]
					except:
						return self.values[fieldName]
				else:
					return ''
			else:
				keys = display.staticOptions.keys()
				keys.sort()

				if self.values.has_key(fieldName):
					return dropDown(name=formFieldName, \
					         values=keys, \
					         titles=[ \
					         display.staticOptions[x] \
					         for x in keys], \
					         default=self.values[ \
					         fieldName])
				else:
					return dropDown(name=formFieldName, \
					         values=keys, \
					         titles=[ \
					         display.staticOptions[x] \
					         for x in keys])
		else:
			assert 0, 'Invalid display.type: ' + display.type
			# This return line exists primarily to make PyChecker
			# happy, but it might serve a useful purpose if
			# assertions are disabled.
			return ''

	def isPrintingField(self, fieldName, arrangement):
		r"""
		Does @a fieldName print in @a arrangement?

		@param fieldName   The field in question.
		@param arrangement The arrangement in question.

		@return A boolean indicating if the field described by
		        @a fieldName prints in @a arrangement.
		"""
		field = self.allFields[fieldName]

		#assert fieldName != 'AccountID', fieldName + ' = ' + str(field.present) + ' ' +\
		#       str(field.visible or field.dbPrimaryKey) + ' ' + \
		#       str(field.arrangements.count(arrangement) > 0)

		return field.present and \
		       field.visible and \
		       field.arrangements.count(arrangement) > 0

	# END getForm Helpers Section

	# START Form Field Holders Section

	## protected:
	def formFieldHolder(cls, label, guts):
		r"""
		Field Holder for the "form" View.

		@param label The form field's label.
		@param guts  The non-label material of the form field.

		@return A table row with one cell holding the @a label and one
		        cell holding the @a guts. This method returns an empty
		        string if @a guts is @c None, the empty string, or
		        consists only of whitespace.
		"""
		__pychecker__ = 'unusednames=cls'

		if guts == None:
			return ''
		guts = guts.strip()
		if guts == '':
			return ''
		return row(cell(label, 'form_row_label') + cell(guts, 'form_row_data'))
	formFieldHolder = classmethod(formFieldHolder)

	def nullFieldHolder(cls, label, guts):
		r"""
		Field Holder for the Form View Helper Functions

		This method simply returns the guts only. This is a "null" form
		field holder, as the name implies, which is used by the "form"
		view generation code.

		@param label The form field's label.
		@param guts  The non-label material of the form field.

		@return @a guts is returned exactly as it was passed.
		"""
		__pychecker__ = 'unusednames=cls,label'
		return guts
	nullFieldHolder = classmethod(nullFieldHolder)

	def listFieldHolder(cls, label, guts):
		r"""
		Field Holder for the "list" View.

		@param label The form field's label.
		@param guts  The non-label material of the form field.

		@return A table row with one cell holding the @a label and one
		        cell holding the @a guts.
		"""
		__pychecker__ = 'unusednames=cls'
		return row(cell(label) + cell(guts))
	listFieldHolder = classmethod(listFieldHolder)

	def rowFieldHolder(cls, label, guts):
		r"""
		Field Holder for the "list" View.

		@param label The form field's label.
		@param guts  The non-label material of the form field.

		@return A table cell holding the @a guts.
		"""
		__pychecker__ = 'unusednames=cls,label'
		return cell(guts, 'rowset_row_data')
	rowFieldHolder = classmethod(rowFieldHolder)
	## public:

	# END Form Field Holders Section

	# START getForm Section

	def getFormTitleRow(self, arrangement=None, editable=False):
		r"""
		Get a table row of titles for all columns.

		@param arrangement The arrangement to get the title row for. If
		                   no @a arrangement is provided, the
		                   @c defaultFieldArrangement will be used.
		@param editable    Will the form that this title row is for be editable?

		@remarks This fails if a field doesn't have a title because
		         the HTML widgetry really wants content.
		"""

		if not arrangement:
			arrangement = self.defaultFieldArrangement

		out = []

		if not editable:
			out.append(cell('', 'rowset_header'))

		for fieldName in self.getPrintingFields(arrangement):
			if self.allFields[fieldName].display:
				customDisplay = self.getDispTitle(fieldName, arrangement, editable)
				if customDisplay != None:
					out.append(cell(customDisplay, 'rowset_header'))
					continue

			out.append(cell(self.allFields[fieldName].title, 'rowset_header'))

		return row(''.join(out))

	def getFormSet(env, structures, editable=False, arrangement=None):
		r"""
		Get a set of forms.

		This method returns a set of forms. getForm() is called for
		each structure in @a structures. Also, a hidden field with the
		@c count of forms is included in the returned data. This
		@c count is used by formLoad() to load the form data back into
		a Structure when the form is submitted.

		@param env         An instance of the @em env class which keeps
		                   track of the current operational
		                   environment.
		@param structures  An iterable variable of structures to return
		                   a form set for.
		@param editable    A boolean indicating if the form should
		                   include elements for editing the fields or
		                   if it should just show the fields.
		@param arrangement The arrangement to get the title row for. If
		                   no @a arrangement is provided, the
		                   @c defaultFieldArrangement will be used.

		@return HTML code representing the various form elements,
		        titles, values, etc.
		"""

		if not arrangement:
			arrangement = structures[0].defaultFieldArrangement

		out = []
		count = 0

		for structure in structures:
			# XXX: This may be considered a kludge.
			if arrangement == 'form' and count:
				out.append(row(cell('<hr />')))

			out.append(structure.getForm(env, editable, \
			                           arrangement, index=count))
			count = count + 1

		if editable:
			# XXX: This creates a two column row, which doesn't
			# XXX: exactly right if we're building a form for the
			# XXX: 'row' arrangement.
			out.append(row(cell('') + cell(hiddenInput( \
			                               structures[0].formPrefix \
						       +'.count', count))))

		return ''.join(out)
	getFormSet = staticmethod(getFormSet)

	def getForm(self, env, editable, arrangement, index=None):
		r"""
		Get a form.

		@param env         An instance of the @em env class which keeps
		                   track of the current operational
		                   environment.
		@param editable    A boolean indicating if the form should
		                   include elements for editing the fields or
		                   if it should just show the fields.
		@param arrangement The arrangement of form to build.
		@param index       The index of this form in relation to other
		                   forms for the same data structure.

		@return HTML form code representing the fields of the
		        Structure in an appropriate containing element (if
			needed) for the current @a arrangement.

		@todo What should the different formats for titling be for
		      different arrangements?  DSL #1, DSL #2, etc...?
		"""
		if arrangement == 'row':
			out = row(self.getFormGuts(env, editable, \
			                            arrangement, index))
		elif arrangement == 'form':
			out = self.getFormGuts(env, editable, \
			                        arrangement, index)
		else:
			out = region(self.formTitle, self.getFormGuts( \
			                                env, editable, \
			                                arrangement, index))

		if editable:
			out += self.getHiddenFormGuts(env, arrangement, index)

		return out

	def getHiddenFormGuts(self, env, arrangement, index):
		r"""
		Get the hidden areas of the form, like the primary key.

		@param env         An instance of the @em env class which keeps track of the current operational environment.
		@param index       The index of this form in relation to other forms for the same data structure.

		@return HTML form code representing the hidden fields of teh structure.
		"""
		out = ''
		
		for fieldName in [x for x in self.findPK() if self.values.has_key(x)]:
			if index == None:
				formFieldName = self.formPrefix + '.' + fieldName
			else:
				formFieldName = self.formPrefix + '.' + fieldName + \
			                 '.' + str(index)

			# If it's not in the arrangement and editable, print it out hidden
			if not (self.allFields[fieldName].arrangements.count(arrangement) > 0 and \
				self.allFields[fieldName].editable):
				out += hiddenInput(formFieldName, self.values[fieldName])

		return out

	## protected:
	def getFormGuts(self, env, editable, arrangement, index):
		r"""
		Get the "guts" of the form.

		Basically, this method calls getFormFieldGuts() for each
		printing field (from getPrintingFields()).

		@param env         An instance of the @em env class which keeps
		                   track of the current operational
		                   environment.
		@param editable    A boolean indicating if the form should
		                   include elements for editing the fields or
		                   if it should just show the fields.
		@param arrangement The arrangement of form to build.
		@param index       The index of this form in relation to other
		                   forms for the same data structure.

		@return HTML form code representing the fields of the structure.
		"""

		out = []

		if arrangement == 'row' and not editable:
			out2 = []
			criterionIndex = 0

			out2.append('<a href="?module=Generic&action=view&arrangement=form&structure=')
			# XXX: This is somewhat of a kludge. If formPrefix is not
			# XXX: the same as the structure's class name, it won't work.
			out2.append(htmlEscape(self.formPrefix))
			for fieldName in self.findPK():
				out2.append('&criterion.')
				out2.append(str(criterionIndex))
				out2.append('=')
				out2.append(htmlEscape(fieldName))
				out2.append('&value.')
				out2.append(str(criterionIndex))
				out2.append('=')
				out2.append(htmlEscape(self.values[fieldName]))
				criterionIndex += 1
			out2.append('">[Details]</a>')
			out.append(cell(''.join(out2), 'rowset_edit_link'))

		for fieldName in self.getPrintingFields(arrangement):
			out.append(self.getFormFieldGuts(env, editable, \
			                             fieldName, \
			                             arrangement, \
			                             index))

		return ''.join(out)

	def getFormFieldGuts(self, env, editable, fieldName, arrangement, \
	                     index, fieldHolderMethod=None):
		r"""
		Get the "guts" of a form field.

		This method uses a @a fieldHolderMethod to format the field's
		title and value into HTML form code.

		@param env               An instance of the @em env class which
		                         keeps track of the current operational
		                         environment.
		@param editable          A boolean indicating if the form
		                         should include elements for editing
		                         the fields or if it should just show
		                         the fields.
		@param fieldName         The name of the field.
		@param arrangement       The arrangement of form to build.
		@param index             The index of this form in relation to
		                         other forms for the same data
		                         structure.
		@param fieldHolderMethod The method to use to format the field.
		                         If no method is provided, the default
		                         method for the @a arrangement will be
		                         used.

		@return HTML form code representing the "guts" of the field's
		        form representation.

		@pre @a fieldName must not be @c None or (convert to via the
		     @c str() built-in) an empty string.

		@pre The type of the field described by @a fieldName must be a
		     supported type unless the field has a @c display function.
		     This shouldn't be a problem as the @em fp constructor
		     should enforce this restriction.
		     Currently supported types are:
		      - bool
		      - cent
		      - decimal
		      - int
		      - date
		      - ip
		      - mac
		      - phone
		      - state
		      - text
		      - zip
		"""

		assert fieldName != None and str(fieldName) != '', \
		       'fieldName must not be None or the emtpy string.'

		field = self.allFields[fieldName]

		if fieldHolderMethod == None:
			if arrangement == 'form':
				fieldHolderMethod = self.formFieldHolder
			elif arrangement == 'list':
				fieldHolderMethod = self.listFieldHolder
			elif arrangement == 'row':
				fieldHolderMethod = self.rowFieldHolder
			else:
				assert 0, \
				      'No support for field arrangement: ' + \
				      arrangement

		if index == None:
			formFieldName = self.formPrefix + '.' + fieldName
		else:
			formFieldName = self.formPrefix + '.' + fieldName + \
			                 '.' + str(index)

		if field.title:
			label = span(htmlEscape(field.title)+': ', \
			             'field_header')
		else:
			label = ''

		if not field.visible:
			# If the field isn't visible, don't bother with any
			# display stuff, just return a hidden field
			return hiddenInput(formFieldName, self.values[fieldName])

		if field.display != None:
			# We have a fancy display element that we have to call
			# getDispElement() on.
			customDisp = self.getDispElement(env, fieldName, formFieldName, (editable and field.editable))

			if customDisp != None:
				return fieldHolderMethod(label, customDisp)

		if field.type == 'bool':
			if self.values.has_key(fieldName):
				value = self.values[fieldName]
			else:
				value = self.allFields[fieldName].dbDefault

			return fieldHolderMethod(label, \
			         checkboxInput(formFieldName, \
				   value, \
			           (editable and field.editable)))

		if field.type == 'cent' or \
		     field.type == 'decimal' or \
		     field.type == 'int' or \
		     field.type == 'date' or \
		     field.type == 'ip' or \
		     field.type == 'mac' or \
		     field.type == 'phone' or \
		     field.type == 'state' or \
		     field.type == 'text' or \
		     field.type == 'zip':
			if self.values.has_key(fieldName):
				value = self.values[fieldName]
			else:
				value = ''

			if field.type == 'cent':
				value = '$' + str(float(value)/100)

			return fieldHolderMethod(label, \
			         textInput(formFieldName, value,
			                   field.length, field.maxlength,
			                   (editable and field.editable)))

		assert 0, 'Unhandled type: ' + field.type
	## public:

	# END getForm Section

	# START Form View Helper Methods

	## protected:
	def getDateAndUserRow(self, dateField, userField, env, editable, \
	                      arrangement, index, autoSetCustomProperty=True):
		r"""
		Get a form row for a corresponding user and date field.

		This method is designed to display the data from two fields
		which correspond to a user event at a particular date. One
		field holds the username and the other field contains the
		date.

		@param dateField             The name of the field which holds
		                             the date information.
		@param userField             The name of the field which holds
		                             the user information.
		@param env                   An instance of the @em env class
		                             which keeps track of the current
		                             operational environment.
		@param editable              A boolean indicating if the form
		                             should include elements for
		                             editing the fields or if it should
		                             just show the fields.
		@param arrangement           The arrangement of form to build.
		                             While this method is designed for
		                             use by the form view, there is
		                             nothing which prevents its use in
		                             other arrangements which might be
		                             created in the future.
		@param index                 The index of this form in realtion
		                             to other forms for the same data
		                             structure.
		@param autoSetCustomProperty A boolean value that will be saved
		                             as the field's @c customFormView
		                             property. This allows subclasses
		                             with custom 'form' views to tell
		                             which fields have been handled by
		                             the custom code. Then, they can
		                             loop through any unhandled fields
		                             applicable to the current
		                             @a arrangement and display them.
		                             The goal of this technique is that
		                             fields may be added to an
		                             @a arrangement that is handled by
		                             custom code at any time and they
		                             will display even if no additional
		                             custom code is written.
		"""

		self.allFields[dateField].customFormView = \
		  autoSetCustomProperty
		self.allFields[userField].customFormView = \
		  autoSetCustomProperty

		fieldHolderMethod = self.nullFieldHolder

		out = []

		if self.isPrintingField(dateField, arrangement):
			out2 = self.getFormFieldGuts(env, editable, \
			                             dateField, arrangement, \
			                             index, \
			                             fieldHolderMethod)
			if out2 != None:
				out2 = out2.strip()
				if out2 != '':
					out.append(out2)
					out.append(' ')

		if self.isPrintingField(userField, arrangement):
			out2 = self.getFormFieldGuts(env, editable, \
			                             userField, arrangement, \
			                             index, \
			                             fieldHolderMethod)
			if out2 != None:
				out2 = out2.strip()
				if out2 != '':
					if self.isPrintingField(dateField, \
					     arrangement):
						out.append(span('by ', \
						               'field_header'))
					out.append(out2)
					out.append(' ')

		if len(out) == 0:
			return ''

		if self.isPrintingField(dateField, arrangement):
			return row(cell(span(htmlEscape( \
			  self.allFields[dateField].title) + ': ', \
			  'field_header'), 'form_row_label') + cell((''.join(out)).strip(), 'form_row_data'))
		elif self.isPrintingField(userField, arrangement):
			return row(cell(span(htmlEscape( \
			  self.allFields[userField].title) + ': ', \
			  'field_header'), 'form_row_label') + cell((''.join(out)).strip(), 'form_row_data'))
		else:
			return ''

	def getSingleItemRow(self, field, env, editable, arrangement, index, \
	                     autoSetCustomProperty=True):
		r"""
		Get a form row for a single item.

		This method is designed to display the data from one field in a
		row by itself.

		@param field                 The name of the field to display.
		@param env                   An instance of the @em env class
		                             which keeps track of the current
		                             operational environment.
		@param editable              A boolean indicating if the form
		                             should include elements for
		                             editing the fields or if it should
		                             just show the fields.
		@param arrangement           The arrangement of form to build.
		                             While this method is designed for
		                             use by the form view, there is
		                             nothing which prevents its use in
		                             other arrangements which might be
		                             created in the future.
		@param index                 The index of this form in realtion
		                             to other forms for the same data
		                             structure.
		@param autoSetCustomProperty A boolean value that will be saved
		                             as the field's @c customFormView
		                             property. This allows subclasses
		                             with custom 'form' views to tell
		                             which fields have been handled by
		                             the custom code. Then, they can
		                             loop through any unhandled fields
		                             applicable to the current
		                             @a arrangement and display them.
		                             The goal of this technique is that
		                             fields may be added to an
		                             @a arrangement that is handled by
		                             custom code at any time and they
		                             will display even if no additional
		                             custom code is written.
		"""

		self.allFields[field].customFormView = autoSetCustomProperty
		if self.isPrintingField(field, arrangement):
			out = self.getFormFieldGuts(env, editable, field, \
			                            arrangement, index)
			if out != None:
				return out
		return ''

	def getMultipleItemRow(self, label, fields, env, editable, \
	                       arrangement, index, autoSetCustomProperty=True):
		r"""
		Get a form row for multiple fields.

		This method is designed to display the data from multiple
		fields in a row. A single @a label will be used for the whole
		row.

		@param label                 The label for the row.
		@param fields                The names of the fields to
		                             display. The fields will be
		                             displayed in the order in which
		                             they are iterated over in
		                             @a fields.
		@param env                   An instance of the @em env class
		                             which keeps track of the current
		                             operational environment.
		@param editable              A boolean indicating if the form
		                             should include elements for
		                             editing the fields or if it should
		                             just show the fields.
		@param arrangement           The arrangement of form to build.
		                             While this method is designed for
		                             use by the form view, there is
		                             nothing which prevents its use in
		                             other arrangements which might be
		                             created in the future.
		@param index                 The index of this form in realtion
		                             to other forms for the same data
		                             structure.
		@param autoSetCustomProperty A boolean value that will be saved
		                             as the field's @c customFormView
		                             property. This allows subclasses
		                             with custom 'form' views to tell
		                             which fields have been handled by
		                             the custom code. Then, they can
		                             loop through any unhandled fields
		                             applicable to the current
		                             @a arrangement and display them.
		                             The goal of this technique is that
		                             fields may be added to an
		                             @a arrangement that is handled by
		                             custom code at any time and they
		                             will display even if no additional
		                             custom code is written.
		"""

		fieldHolderMethod = self.nullFieldHolder
		out = []
		for field in fields:
			self.allFields[field].customFormView = \
			  autoSetCustomProperty
			if self.isPrintingField(field, arrangement):
				out2 = self.getFormFieldGuts(env, editable, \
				         field, arrangement, index, \
				         fieldHolderMethod)
				if out2 != None:
					out2 = out2.strip()
					if out2 != '':
						out.append(out2)
						out.append(' ')
		if len(out) > 0:
			if label != None and label != '':
				return row(cell(span(htmlEscape(label) + ': ', 'field_header'), 'form_row_label')
				         + cell((''.join(out)).strip(), 'form_row_data'))
			else:
				return row(cell('', 'form_row_label') + \
				  cell((''.join(out)).strip(), 'form_row_data'))
		else:
			return ''

	def getMultipleLabeledItemRow(self, label, items, env, editable, \
	                              arrangement, index, labelPlacement=0, \
	                              multiLine=False,
	                              autoSetCustomProperty=True):
		r"""
		Get a form row for multiple items, each with its own label.

		This method is designed to display the data from multiple
		fields in a row. A single @a label will be used for the whole
		row. Each item will also have a label.

		@param label                 The label for the row.
		@param items                 The items to display. Each item
		                             must be a tuple (or list) of one
		                             or two elements. The first element
		                             is the value. The optional second
		                             element is the label for the item.
		                             If no label is specified, the
		                             item's @c title will be used. The
					     items will be displayed in the
		                             order in which they are iterated
		                             over in @a items.
		@param env                   An instance of the @em env class
		                             which keeps track of the current
		                             operational environment.
		@param editable              A boolean indicating if the form
		                             should include elements for
		                             editing the fields or if it should
		                             just show the fields.
		@param arrangement           The arrangement of form to build.
		                             While this method is designed for
		                             use by the form view, there is
		                             nothing which prevents its use in
		                             other arrangements which might be
		                             created in the future.
		@param index                 The index of this form in realtion
		                             to other forms for the same data
		                             structure.
		@param labelPlacement        If @a labelPlacement is @c 0, the
		                             labels will be placed in front of
		                             the data. If @a labelPlacement is
		                             @c 1, the labels will be placed
		                             after the data.
		@param multiLine             If true, each item will be have
		                             its own row in a sub-table.
		@param autoSetCustomProperty A boolean value that will be saved
		                             as the field's @c customFormView
		                             property. This allows subclasses
		                             with custom 'form' views to tell
		                             which fields have been handled by
		                             the custom code. Then, they can
		                             loop through any unhandled fields
		                             applicable to the current
		                             @a arrangement and display them.
		                             The goal of this technique is that
		                             fields may be added to an
		                             @a arrangement that is handled by
		                             custom code at any time and they
		                             will display even if no additional
		                             custom code is written.

		@pre @a labelPlacement must be zero or one.
		"""
		assert (labelPlacement == 0 or labelPlacement == 1), \
		       'labelPlacement must be zero or one.'

		fieldHolderMethod = self.nullFieldHolder
		out = []
		for item in items:
			if len(item) == 2:
				field = item[0]
				itemLabel = item[1]
			elif len(item) == 1:
				field = item[0]
				itemLabel = self.allFields[field].title
			else:
				assert 0, "Invalid length item tuple."

			self.allFields[field].customFormView = \
			  autoSetCustomProperty

			if itemLabel == None:
				itemLabel = ''
			else:
				itemLabel = itemLabel.strip()

			if self.isPrintingField(field, arrangement):
				out2 = self.getFormFieldGuts(env, editable, \
				         field, arrangement, index, \
					 fieldHolderMethod)

				if out2 == None:
					continue

				out2 = out2.strip()

				if out2 == '':
					continue

				out3 = []
				out4 = []

				if itemLabel != '':
					if labelPlacement == 0:
						out3.append(span( \
						  htmlEscape( \
						   itemLabel) + ': ', \
						  'field_header'))
						out3.append(' ')
					
					if labelPlacement == 1:
						out4.append(span('(' + \
						  htmlEscape( \
						   itemLabel) + ')', \
						  'field_header'))
						out4.append(' ')

				if multiLine:
					if labelPlacement == 0:
						out.append(row(cell(''.join(out3) + ' ') + cell(out2)))
					else:
						out.append(row(cell(out2 + ' ') + cell(''.join(out4))))
				else:
					out.extend(out3)
					out.append(out2)
					out.append(' ')
					out.extend(out4)

		if len(out) > 0:
			temp = (''.join(out)).strip()
			if label != None and label != '':
				if multiLine:
					temp = '\n' + table(label, temp,
					                    cellpadding=2)
				return row(cell(span(htmlEscape(label) + \
				                     ': ', 'field_header'), 'form_row_label') \
				         + cell(temp, 'form_row_data'))
			else:
				if multiLine:
					temp = '\n' + table('', temp,
					                    cellpadding=2)
				return row(cell('', 'form_row_label') + \
				  cell(temp, 'form_row_data'))
		else:
			return ''


	def getMultipleLabeledItemBlock(self, label, items, env, editable, \
	                                arrangement, index, labelPlacement=0, \
	                                columns=3,
	                                autoSetCustomProperty=True):
		r"""
		Get a form row for multiple items, each with its own label,
		formatted in a block.

		This method is designed to display the data from multiple
		fields in a block form, within the normal form row. A single
		@a label will be used for the whole row. Each item will also
		have a label.

		@param label                 The label for the block.
		@param items                 The items to display. Each item
		                             must be a tuple (or list) of one
		                             or two elements. The first element
		                             is the value. The optional second
		                             element is the label for the item.
		                             If no label is specified, the
		                             item's @c title will be used. The
					     items will be displayed in the
		                             order in which they are iterated
		                             over in @a items.
		@param env                   An instance of the @em env class
		                             which keeps track of the current
		                             operational environment.
		@param editable              A boolean indicating if the form
		                             should include elements for
		                             editing the fields or if it should
		                             just show the fields.
		@param arrangement           The arrangement of form to build.
		                             While this method is designed for
		                             use by the form view, there is
		                             nothing which prevents its use in
		                             other arrangements which might be
		                             created in the future.
		@param index                 The index of this form in realtion
		                             to other forms for the same data
		                             structure.
		@param labelPlacement        If @a labelPlacement is @c 0, the
		                             labels will be placed in front of
		                             the data. If @a labelPlacement is
		                             @c 1, the labels will be placed
		                             after the data.
		@param columns               The number of columns to be used
		                             when creating the block.
		@param autoSetCustomProperty A boolean value that will be saved
		                             as the field's @c customFormView
		                             property. This allows subclasses
		                             with custom 'form' views to tell
		                             which fields have been handled by
		                             the custom code. Then, they can
		                             loop through any unhandled fields
		                             applicable to the current
		                             @a arrangement and display them.
		                             The goal of this technique is that
		                             fields may be added to an
		                             @a arrangement that is handled by
		                             custom code at any time and they
		                             will display even if no additional
		                             custom code is written.

		@pre @a labelPlacement must be zero or one.
		"""
		assert (labelPlacement == 0 or labelPlacement == 1), \
		       'labelPlacement must be zero or one.'

		fieldHolderMethod = self.nullFieldHolder

		for item in items:
			self.allFields[item[0]].customFormView = \
			  autoSetCustomProperty

		items = [x for x in items
		            if self.isPrintingField(x[0], arrangement)]

		out = []

		for i in xrange(math.ceil(float(len(items)) / columns)):
			out2 = []
			for j in xrange(columns):

				if i*columns+j >= len(items):
					break

				out3 = []
			
				item = items[i*columns+j]

				if len(item) == 2:
					field = item[0]
					itemLabel = item[1]
				elif len(item) == 1:
					field = item[0]
					itemLabel = self.allFields[field].title
				else:
					assert 0, "Invalid length item tuple."

				if itemLabel == None:
					itemLabel = ''
				else:
					itemLabel = itemLabel.strip()

				out4 = self.getFormFieldGuts(env, editable, \
				         field, arrangement, index, \
					 fieldHolderMethod)

				if out4 == None:
					out2.append(cell(''))
					continue

				out4 = out4.strip()

				if out4 == '':
					out2.append(cell(''))
					continue

				if itemLabel != '':
					if labelPlacement == 0:
						out3.append(span( \
						  htmlEscape( \
						   itemLabel) + ': ', \
						  'field_header'))
						out3.append(' ')

					out3.append(out4)

					if labelPlacement == 1:
						out3.append(span('(' + \
						  htmlEscape( \
						   itemLabel) + ')', \
						  'field_header'))
						out3.append(' ')

				out2.append(cell((''.join(out3)).strip()))

			out.append(row((''.join(out2)).strip()))

		return row(cell(span(htmlEscape(label) + ': ',
		  'field_header'), 'form_row_label') + cell(
		  table(label, (''.join(out)).strip()), 'form_row_data'))

	## public:

	# END Form View Helper Methods
