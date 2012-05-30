class fp:
	r"""
	Contains Field Properties

	This class stores a variety of properties for the fields in a
	Structure instance. These properties include everything from if a given
	field is present in the current configuration to what type of data may
	be stored in a field to how a field will be displayed, stored, etc.

	The variables are stored by the same name they are passed to the
	constructor. Currently, they are designed to be read directly (without
	accessor methods). While no code prevents the modification of these
	variables or the storage of other variables, consumers of this class
	are strongly discouraged from modifying any variables of this class.
	One exception exists, however: The @c customFormView variable exists
	for use by a subclass reimplementation of
	Structure::Structure::getFormGuts().

	This variable is intended for use as a temporary variable and consumers
	of this class must not rely upon the state of this variable being
	maintained between method calls or even that its state will suitably
	initialized.

	@author Andy Filer \<andyf\@wiktel.com\>
	@author Richard Laager \<rlaager\@wiktel.com\>
	"""

	def __init__(self,
	  type='text',
	  display=None,
	  title='',
	  length=None,
	  present=True,
	  visible=True,
	  editable=True,
	  arrangements=['form', 'list'],
	  dbConstraint=None,
	  dbDefault=None,
	  dbDynamicProperty=False,
	  dbForeignKey=None,
	  dbForeignTable=None,
	  dbIdentity=False,
	  dbIndexed=False,
	  dbName=None,
	  dbNulls=False,
	  dbPrimaryKey=False,
	  dbType=None,
	  dbUnique=False,
	  ffOffset=None,
	  ffGarbage=None,
	  maxlength=None,
	  minimum=None,
	  maximum=None):
		r"""
		@param type           The type of the field. Valid types are:
		                       - @c bool Boolean
				       - @c cent Monetary Value (expressed in
		                                 cents -- for COBOL
		                                 compatibility)
		                       - @c date Date/Time
		                       - @c decimal Decimal Number
		                       - @c email E-Mail Address
		                       - @c int Integer
		                       - @c ip IP Address
		                       - @c mac Network MAC Address
		                       - @c money Monetary Value (expressed in
		                                 a decimal dollar amount)
		                       - @c phone Phone Number
		                       - @c state State/Province Two-Letter
		                                  Abbreviation
		                       - @c text Free Text Field
		                       - @c zip USPS Zip Code (Optionally
		                                the Zip+4 Code)
		@param display        A reference to an instance of the
		                      disp::disp class. This instance will
		                      define information used to generate the
		                      displayed version of the field. (The most
		                      common example of such a customized
		                      display would be drop-down menus.)
		@param title          The title of the field. If @c None is
		                      supplied, it is equivalent to supplying
		                      the empty string. Otherwise, the supplied
		                      value is converted into a string (using
		                      the str() built-in) for storage.
		@param length         The length to use when displaying a form
		                      element for this field. This only affects
		                      the length of the displayed form element
		                      and not the amount of data which may be
		                      entered. If @a length is @c None, an
		                      appropriate default will be set when
		                      possible.
		@param present        A boolean indicating if the field is
		                      present in the current configuration.
		@param visible        A boolean indicating if the field should
		                      be visible to the user in the current
		                      configuration.
		@param editable       A boolean indicating if the field should
		                      be editable by the user in the current
		                      configuration.
		@param arrangements   A list of form arrangements for which the
		                      field should be displayed. Valid
		                      arrangements are:
		                       - form
		                       - list
		                       - row
		@param dbConstraint   A string containing an SQL conditional
		                      expression. This expression will be saved
		                      as a database constraint for this field.
		                      The question mark shall be used in place
		                      of the field's database name. (This
		                      allows the database name of the field to
		                      be changed without the need to update all
		                      database constraints.)
		@param dbDefault      The default value to use for the field.
		                      This may be either a constant value or a
		                      SQL expression. (For example,
		                      @c 'getdate()' could be used as the
		                      @a dbDefault to automatically fill in a
		                      field with the date it is inserted into
		                      the database if no date is provided.)
		@param dbDynamicProperty A boolean indicating if the field is
		                         a dynamic property stored in a
		                         separate table.
		@param dbForeignKey   The name of the referenced column in a
		                      foreign key relationship. Typically,
		                      this is not needed when creating a
		                      foreign key relationship because the
		                      columns will have the same name.
		@param dbForeignTable A reference to a Structure::Structure
		                      class for the referenced table in a
		                      foreign key relationship.
		@param dbIdentity     A boolean indicating if the field is
		                      stored in the database as an @c IDENTITY
		                      (auto-incrementing) column.
		@param dbIndexed      A boolean indicating if the field is to
		                      be indexed in the database.
		@param dbName         The name of the field in the database.
		@param dbNulls        A boolean indicating if @c NULL is to be
		                      allowed for this field in the database.
		@param dbPrimaryKey   A boolean indicating if the field is
		                      (part of) a primary key in the database.
		@param dbType         The database type of the field. If
		                      @a dbType is @c None, a default database
		                      type will be set based upon @a type.
		@param dbUnique       A boolean indicating if the field must
		                      be unique in the database.
		@param ffOffset       An integer indicating the offset (in
		                      bytes) of the field relative to the start
		                      of the record. (This property is not
		                      typically used because it is easier to
		                      automatically calculate the field
		                      offsets.)
		@param ffGarbage      A boolean indicating if the field is
		                      mid-record garbage which is to be
		                      ignored. (This property exists to allow
		                      field offsets to be automatically
		                      calculated by
		                      FlatFileStructure::FlatFileStructure.)
		@param maxlength      The maximum length (in characters) of the
		                      field.
		@param minimum        The minimum numeric value which may be
		                      stored in the field. This value, if
		                      present, will be added to the
		                      @a dbConstraint property so that it will
		                      be enforced by the database.
		@param maximum        The maximum numeric value which may be
		                      stored in the field. This value, if
		                      present, will be added to the
		                      @a dbConstraint property so that it will
		                      be enforced by the database.

		@pre @a type must be a valid type listed above.
		@pre @a arrangements must contain at least one element if
		     @a visible is true.
		@pre @a arrangements must only contain valid arrangements
		     listed above.
		@pre @a arrangements must not contain duplicate arrangement
		     elements.

		@post @a arrangments is filled with all arrangment types when
		      @a visible is false and @a dbPrimaryKey is true.
		@post @a length is implied by @a type in some cases when
		      @a length is @c None.
		@post @a dbType is implied by @a type when @a dbType is
		      @c None.
		@post @a dbIndexed is implied by @a dbPrimaryKey.
		@post @a dbUnique is implied by @a dbPrimaryKey.
		@post @a dbNulls is prohibited by @a dbIndexed.
		@post @a maxlength is implied by @a type in some cases when
		      @a maxlength is @c None.
		@post @a maxlength is implied by @a dbType in some cases when
		      @a maxlength is @c None.
		@post @a maxlength will be clamped to database maximums.
		@post @a dbConstraint will have code added to enforce a minimum
		      value if @a minimum is not @c None.
		@post @a dbConstraint will have code added to enforce a maximum
		      value if @a maximum is not @c None.
		@post @a minimum will be set for all numeric database types. It
		      will be the larger of the specified @a minimum and the
		      minimum the database can store for the database type of
		      the field.
		@post @a maximum will be set for all numeric database types. It
		      will be the smaller of the specified @a maximum and the
		      maximum the database can store for the database type of
		      the field.

		@remarks Consumers of this class must be aware that the order
		         of arguments to the constructor is not guaranteed.
		         Callers arestronly advised to pass arguments by name.
		"""

		assert \
			   type == 'bool' \
			or type == 'cent' \
			or type == 'date' \
			or type == 'decimal' \
			or type == 'email' \
			or type == 'int' \
			or type == 'ip' \
			or type == 'mac' \
			or type == 'money' \
			or type == 'phone' \
			or type == 'state' \
			or type == 'text' \
			or type == 'zip', \
			'Invalid type: ' + type
		self.type = intern(type)

		self.display = display

		# Display Attributes
		if title != None:
			self.title = str(title)
		else:
			self.title = ''

		if length != None:
			self.length = length
		elif self.type == 'date':
			self.length = 24
		elif self.type == 'ip':
			self.length = 15
		elif self.type == 'mac':
			self.length = 17
		elif self.type == 'phone':
			self.length = 12
		elif self.type == 'state':
			self.length = 2
		elif self.type == 'text':
			self.length = 25
		elif self.type == 'zip':
			self.length = 10
		else:
			self.length = 0

		self.present  = bool(present)
		self.visible  = bool(visible)
		self.editable = bool(editable)

		assert (not self.visible) or \
		       (arrangements != None and len(arrangements) > 0), \
		       'No arrangements specified.'

		for arrangement in arrangements:
			assert arrangement == 'form' or \
			       arrangement == 'list' or \
			       arrangement == 'row', \
			       'Invalid arrangement: ' + arrangement

		assert arrangements.count('form') <= 1 and \
		       arrangements.count('list') <= 1 and \
		       arrangements.count('row')  <= 1, \
		       'Duplicate arrangements are not allowed.'

		self.arrangements = arrangements

		self.customFormView = False

		# Database Attributes
		self.dbConstraint = dbConstraint

		self.dbDefault = dbDefault

		self.dbDynamicProperty = dbDynamicProperty

		self.dbForeignKey = dbForeignKey
		self.dbForeignTable = dbForeignTable

		self.dbIdentity = bool(dbIdentity)

		self.dbIndexed = bool(dbIndexed)

		self.dbName = dbName

		self.dbNulls = bool(dbNulls)

		if dbType != None:
			self.dbType = dbType
		else:
			if   self.type == 'bool':
				self.dbType = 'bit'
			elif self.type == 'cent':
				# XXX: This shouldn't ever really be necessary
				# because the type 'cent' is for flat files.
				self.dbType = 'money'
			elif self.type == 'date':
				self.dbType = 'smalldatetime'
			elif self.type == 'decimal':
				self.dbType = 'decimal'
			elif self.type == 'email':
				self.dbType = 'varchar'
			elif self.type == 'int':
				self.dbType = 'integer'
			elif self.type == 'ip':
				self.dbType = 'varchar'
			elif self.type == 'mac':
				self.dbType = 'varchar'
			elif self.type == 'money':
				self.dbType = 'money'
			elif self.type == 'phone':
				self.dbType = 'varchar'
			elif self.type == 'state':
				self.dbType = 'varchar'
			elif self.type == 'text':
				self.dbType = 'varchar'
			elif self.type == 'zip':
				self.dbType = 'varchar'
			else:
				# If this assertion is triggered, it means that
				# a new type was added without adding the code
				# here to set a default dbType for it.
				assert 0, 'Unhandled type: ' + self.type

		self.dbType = intern(self.dbType)

		self.dbUnique = bool(dbUnique)

		self.dbPrimaryKey = bool(dbPrimaryKey)
		if self.dbPrimaryKey:
			# dbIndexed is implied by dbPrimaryKey
			self.dbIndexed = True
			# dbUnique is implied by dbPrimaryKey
			self.dbUnique = True

		if self.dbUnique:
			# dbNulls is implicitly prohibited by dbUnique
			self.dbNulls = False

		if self.dbType == 'bit' and \
		   self.dbDefault == None and \
		   not self.dbNulls:
			self.dbDefault='0'

		if self.dbDynamicProperty:
			dbNulls = True

			assert dbConstraint == None, \
			  'dbConstraint is incompatible with dynamic properties.'
			assert dbDefault == None, \
			  'dbDefault is incompatible with dynamic properties.'
			assert dbForeignKey == None, \
			  'dbForeignKey is incompatible with dynamic properties.'
			assert dbForeignTable == None, \
			  'dbForeignTable is incompatible with dynamic properties.'
			assert dbIdentity == False, \
			  'dbIdentity is incompatible with dynamic properties.'
			assert dbIndexed == False, \
			  'dbIndexed is incompatible with dynamic properties.'
			assert dbPrimaryKey == False, \
			  'dbPrimaryKey is incompatible with dynamic properties.'
			assert dbUnique == False, \
			  'dbUnique is incompatible with dynamic properties.'

		self.ffOffset = ffOffset
		self.ffGarbage = ffGarbage

		# Constraints
		if maxlength != None:
			self.maxlength = maxlength
		elif self.type == 'date':
			self.maxlength = 24
		elif self.type == 'ip':
			self.maxlength = 15
		elif self.type == 'mac':
			self.maxlength = 17
		elif self.type == 'phone':
			self.maxlength = 14
		elif self.type == 'zip':
			self.maxlength = 10
		elif self.dbType == 'char' or \
		     self.dbType == 'nchar' or \
		     self.dbType == 'varchar' or \
		     self.dbType == 'nvarchar':
			self.maxlength = 255
		else:
			self.maxlength = None

		if   self.dbType == 'char' or \
		     self.dbType == 'varchar':
			self.maxlength = min(self.maxlength, 8000)
		elif self.dbType == 'nchar' or \
		     self.dbType == 'nvarchar':
			self.maxlength = min(self.maxlength, 4000)

		if minimum != None or maximum != None:
			if minimum != None:
				minConstraint = '[' + self.dbName + '] >= ' + \
				                str(minimum)
			else:
				minConstraint = None

			if maximum != None:
				maxConstraint = '[' + self.dbName + '] <= ' + \
				                str(maximum)
			else:
				maxConstraint = None

			if dbNulls:
				tempConstraint = '([' + self.dbName + \
				                 '] IS NULL OR ('
			else:
				tempConstraint = ''

			if minConstraint != None:
				tempConstraint += minConstraint
				if maxConstraint != None:
					tempConstraint += ' AND ' + \
					                  maxConstraint
			elif maxConstraint != None:
				tempConstraint += maxConstraint
			else:
				assert 0, 'This code should never execute.'

			if dbNulls:
				tempConstraint += '))'

			if self.dbConstraint != None and \
			   dbDynamicProperty == False:
				self.dbConstraint = tempConstraint + \
				                    ' AND (' + \
				                    self.dbConstraint + ')'
			else:
				self.dbConstraint = tempConstraint

		self.minimum = None
		self.maximum = None

		if   self.dbType == 'bigint':
			self.minimum = -2**63
			self.maximum =  2**63 - 1
		elif self.dbType == 'int':
			self.minimum = -2**31
			self.maximum =  2**31 - 1
		elif self.dbType == 'smallint':
			self.minimum = -2**15
			self.maximum =  2**15 - 1
		elif self.dbType == 'tinyint':
			self.minimum = 0
			self.maximum = 255
		elif self.dbType == 'decimal' or \
		     self.dbType == 'numeric':
			self.minimum = -10**38 + 1
			self.maximum =  10**38 - 1
		elif self.dbType == 'money':
			self.minimum = -922,337,203,685,477.5808
			self.maximum =  922,337,203,685,477.5807
		elif self.dbType == 'smallmoney':
			self.minimum = -214,748.3648
			self.maximum =  214,748.3647

		self.minimum = max(self.minimum, minimum)
		self.maximum = min(self.maximum, maximum)
