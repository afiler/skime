class disp:
	r"""
	Complex field display information
	"""
	def __init__(self, type=None, table=None, displayField=None, dataField=None, staticOptions=None, query=None, where=None):
		if type != None:
			assert \
				   type == 'dbDropdown' \
				or type == 'dbLookup' \
				or type == 'staticDropdown', \
				'Invalid type: ' + type
			self.type = intern(type)
		else:
			raise AttributeError, 'type must not be None'

		self.type=type

		if self.type == 'dbDropdown':
			assert table != None, 'table must not be None if type is dbDropdown'
			assert displayField != None, 'displayField must not be None if type is dbDropdown'
			assert dataField != None, 'dataField must not be None if type is dbDropdown'
			assert staticOptions == None, 'staticOptions is not applicable for a dbDropdown type'

		if self.type == 'dbLookup':
			assert table != None, 'table must not be None if type is dbLookup'
			assert displayField != None, 'displayField must not be None if type is dbLookup'
			assert dataField != None, 'dataField must not be None if type is dbLookup'
			assert staticOptions == None, 'staticOptions is not applicable for a dbLookup type'

		if self.type == 'staticDropdown':
			assert table == None, 'table is not applicable for a staticDropdown type'
			assert displayField == None, 'displayField is not applicable for a staticDropdown type'
			assert dataField == None, 'dataField is not applicable for a staticDropdown type'
			assert query == None, 'query is not applicable for a staticDropdown type'
			assert where == None, 'where is not applicable for a staticDropdown type'

		self.table = table
		self.displayField = displayField
		self.dataField = dataField
		self.query = query
		self.where = where

		self.staticOptions=staticOptions
