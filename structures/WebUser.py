from Structure import *
from structures.InternalUser import InternalUser
from structures.SubAccount import SubAccount
from structures.Web import Web

class WebUser(Structure):

	def __init__(self, env):
		r"""
		Initialize a WebUser.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'WebUserID': fp(
				type='int',
				title='Web User ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='WebUserID',
				dbPrimaryKey=True,
			),
			'WebID': fp(
				type='int',
				display=disp(type='dbDropdown', table=Web, displayField='Name', dataField='WebID'),
				title='Web ID',
				arrangements=['form', 'list', 'row'],
				dbForeignTable=Web,
				dbIndexed=True,
				dbName='WebID',
			),
			'AccountID': fp(
				type='int',
				display=disp(type='dbLookup', table=SubAccount, displayField='Username', dataField='AccountID'),
				title='Account ID',
				arrangements=['form', 'list', 'row'],
				dbForeignTable=SubAccount,
				dbIndexed=True,
				dbName='AccountID',
			),
			'Administrator': fp(
				type='bool',
				title='Admin',
				arrangements=['form', 'list', 'row'],
				dbName='Administrator',
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
			'WebUserID',
			'WebID',
			'AccountID',
			'Administrator',
			'CreateDate',
			'CreateUser',
		)

		Structure.__init__(self,
		                   'WebUsers',
		                   'WebUser',
		                   'Web User',
		                   'Web Users')

		if env != None and env.configWebUser:
			env.configWebUser(self)

		self.buildFields()

		if (self.allFields['AccountID'].present and \
		    self.allFields['WebID'].present):
			self.dbConstraints += 'UNIQUE ([' + \
			  self.allFields['AccountID'].dbName + '],[' + \
			  self.allFields['WebID'].dbName + ']),\n'
