from datamodules.action import action
from datamodules.DataModule import DataModule
from structures.Search import Search

from structures.MasterAccount import MasterAccount
from structures.DSLAccount import DSLAccount
from structures.SubAccount import SubAccount
from structures.SubWeb import SubWeb
from structures.Web import Web
from structures.WebRedirect import WebRedirect
from structures.WirelessAccount import WirelessAccount

class GeneralSearch(DataModule):

	def __init__(self, env):
		self.moduleName = "GeneralSearch"

		self.actions = {"searchform":	action(loadFromForm=0, editable=1, nextAction="search", nextTitle="Search >>"),
				"search":	action(queryFromForm=1, editable=0, nextModule="CustomerRecord", nextAction="view", nextLink=1) }

		self.structures = {GeneralSearchStructure: {}}
		self.rootStructure = GeneralSearchStructure
		self.data = []
		self.extraVars = []
		self.arrangement = None
		self.pageTitle = "Search"

class GeneralSearchStructure(Search):

	def __init__(self, env):
		self.env = env

		# This is the definition of the data structure
		# Its format is { (Table, 'Key'): { Optional (Foreign Table, 'Key'): {} } }
		# etc recursively.
		# The results are flattened into one table.
		self.fieldStruct = {	(MasterAccount, 'CustomerID'):
					{
						(SubAccount, 'Username'): {},
						(SubAccount, 'Password'): {}
					},
					(MasterAccount, 'FirstName'): {},
					(MasterAccount, 'LastName'): {},
					(MasterAccount, 'BillingNumber'): {}
				}

		(self.fieldSet, self.tableNames, self.joins) = self.getFieldsAndTables(self.fieldStruct)

		#TEMP
		self.fieldOrder = [y for x, y, z in self.fieldSet]
		self.fieldOrder = ('CustomerID', 'Username', 'BillingNumber', 'FirstName', 'LastName')

		self.dbTable    = 'MasterAccount'
		self.formPrefix = 'Search'
		self.formTitle  = 'Search'
		self.groupTitle = 'Search'
		self.pageTitle  = 'Search'

		self.defaultFieldArrangement = 'row'

		# fieldSet contains table names, field fp objects, and field names,
		# so build allFields from this
		self.allFields = {}
		for x in self.fieldSet: self.allFields[x[2]] = x[1]

		self.values = {}

		# This is done on every Structure
		self.buildFields()