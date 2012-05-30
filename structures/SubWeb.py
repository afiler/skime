from Structure import *
from structures.InternalUser import InternalUser
from structures.MasterAccount import MasterAccount
from structures.Web import Web

class SubWeb(Structure):

	def __init__(self, env):
		r"""
		Initialize a SubWeb.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'SubWebID': fp(
				type='int',
				title='SubWeb ID',
				editable=False,
				dbIdentity=True,
				dbName='SubWebID',
				dbPrimaryKey=True,
			),
			'CustomerID': fp(
				type='int',
				title='Customer ID',
				arrangements=['form', 'list', 'row'],
				dbForeignTable=MasterAccount,
				dbIndexed=True,
				dbName='CustomerID',
			),
			'WebID': fp(
				type='int',
				display=disp(type='dbDropdown',
				             table=Web,
				             displayField='Name',
				             dataField='WebID'),
				title='Web',
				arrangements=['form', 'list', 'row'],
				dbForeignTable=Web,
				dbIndexed=True,
				dbName='WebID',
			),
			'Name': fp(
				title='SubWeb Name',
				arrangements=['form', 'list', 'row'],
				dbIndexed=True,
				dbName='SubWebName',
				maxlength=50,
			),
			'DiskQuota': fp(
				type='int',
				title='Disk Quota',
				arrangements=['form', 'list', 'row'],
				dbNulls=True,
				dbName='DiskQuota',
				minimum=0,
			),
			'Description': fp(
				title='Description',
				dbName='Description',
				dbNulls=True,
			),
			'ListInDirectory': fp(
				type='bool',
				title='List in Directory',
				dbName='ListInDirectory',
			),
			'Active': fp(
				type='bool',
				title='Active',
				arrangements=['form', 'list', 'row'],
				dbDefault='1',
				dbName='Active',
			),
			'FrontPage': fp(
				type='bool',
				title='FrontPage',
				arrangements=['form', 'list', 'row'],
				dbName='FrontPage',
			),
			'CreateDate': fp(
				type='date',
				title='Created',
				editable=False,
				dbDefault='getdate()',
				dbName='CreateDate',
			),
			'CreateUser': fp(
				type='int',
				title='Created By',
				editable=False,
				dbForeignKey='InternalUserID',
				dbForeignTable=InternalUser,
				dbName='CreateUser',
			),
		}

		self.fieldOrder = (
			'SubWebID',
			'CustomerID',
			'WebID',
			'Name',
			'ListInDirectory',
			'Description',
			'Active',
			'DiskQuota',
			'FrontPage',
			'CreateDate',
			'CreateUser',
		)

		self.dbTable    = "SubWebs"
		self.formPrefix = "SubWeb"
		self.formTitle  = "SubWeb"
		self.groupTitle = "SubWebs"

		self.defaultFieldArrangement = 'row'

		Structure.__init__(self,
		                   'SubWebs',
		                   'SubWeb',
		                   'Sub Web',
		                   'Sub Webs',
				   'row')

		if env != None and env.configSubWeb:
			env.configSubWeb(self)

		self.buildFields()

		if (self.allFields['Name'].present and \
		    self.allFields['WebID'].present):
			self.dbConstraints += 'UNIQUE ([' + \
			  self.allFields['Name'].dbName + '],[' + \
			  self.allFields['WebID'].dbName + ']),\n'

		if self.allFields['Description'].present and \
		   self.allFields['ListInDirectory'].present:
			self.dbConstraints += 'CONSTRAINT [CK_' + \
			  self.dbTable + '_' + \
			  self.allFields['Description'].dbName + '_' + \
			  self.allFields['ListInDirectory'].dbName + \
			  '] CHECK ([' + \
			  self.allFields['ListInDirectory'].dbName + \
			  '] = 0 OR ([' + \
			  self.allFields['Description'].dbName + \
			  '] IS NOT NULL AND RTRIM(LTRIM([' + \
			  self.allFields['Description'].dbName + \
			  "])) <> '')),\n"
