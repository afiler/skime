from Structure import *
from structures.InternalUser import InternalUser
from structures.SubAccount import SubAccount
from structures.SubWeb import SubWeb

class SubWebUser(Structure):

	def __init__(self, env):
		r"""
		Initialize a SubWebUser.

		@param env An instance of the @em env class which keeps track
		           of the current operational environment.
		"""
		self.allFields = {
			'SubWebUserID': fp(
				type='int',
				title='SubWeb User ID',
				visible=False,
				editable=False,
				dbIdentity=True,
				dbName='SubWebUserID',
				dbPrimaryKey=True,
			),
			'SubWebID': fp(
				type='int',
				title='SubWeb ID',
				dbForeignTable=SubWeb,
				dbIndexed=True,
				dbName='SubWebID',
			),
			'AccountID': fp(
				type='int',
				title='Account ID',
				dbForeignTable=SubAccount,
				dbIndexed=True,
				dbName='AccountID',
			),
			'Administrator': fp(
				type='bool',
				title='Web Administrator',
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
			'SubWebUserID',
			'SubWebID',
			'AccountID',
			'Administrator',
			'CreateDate',
			'CreateUser',
		)

		Structure.__init__(self,
		                   'SubWebUsers',
		                   'SubWebUser',
		                   'SubWeb User',
		                   'SubWeb Users')

		if env != None and env.configSubWebUser:
			env.configSubWebUser(self)

		self.buildFields()

		if (self.allFields['AccountID'].present and \
		    self.allFields['SubWebID'].present):
			self.dbConstraints += 'UNIQUE ([' + \
			  self.allFields['AccountID'].dbName + '],[' + \
			  self.allFields['SubWebID'].dbName + ']),\n'
